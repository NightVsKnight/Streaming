import obspython as obs
import re
import datetime

ROTATION_SOURCES_VAR = "RotationSources"
ROTATION_INDEX_VAR = "RotationIndex"
ROTATION_RUNNING_VAR = "RotationRunning"
ROTATION_FALLBACK_VAR = "RotationSceneFallback"


def _log(level, msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    obs.script_log(level, f"[InlineRotate {ts}] {msg}")


def parse_source_list(value):
    if not value:
        return []
    matches = re.findall(r'"([^"]+)"', value)
    if matches:
        return [m.strip() for m in matches if m.strip()]
    return [part.strip().strip('"').strip() for part in value.split(",") if part.strip().strip('"').strip()]


def get_source_dimensions(name):
    src = obs.obs_get_source_by_name(name)
    if src is None:
        _log(obs.LOG_WARNING, f"Source '{name}' not found; skipping")
        return 0, 0
    try:
        return obs.obs_source_get_width(src), obs.obs_source_get_height(src)
    finally:
        obs.obs_source_release(src)


def find_next_valid_index(names, current_index):
    if not names:
        return None
    for offset in range(1, len(names) + 1):
        idx = (current_index + offset) % len(names)
        w, h = get_source_dimensions(names[idx])
        if w > 0 and h > 0:
            _log(obs.LOG_INFO, f"Next source candidate '{names[idx]}' at index {idx} ({w}x{h})")
            return idx
        _log(obs.LOG_INFO, f"Skipping '{names[idx]}' (index {idx}) — size {w}x{h}")
    return None


def _set_sceneitem_visibility_recursive(scene, scene_name, source_name, visible, disable):
    items = obs.obs_scene_enum_items(scene)
    if items is None:
        return False
    try:
        for item in items:
            src = obs.obs_sceneitem_get_source(item)
            if src is None:
                continue
            src_name = obs.obs_source_get_name(src)
            _log(obs.LOG_DEBUG, f"Inspecting '{src_name}' while searching for '{source_name}' in '{scene_name}'")
            if src_name == source_name:
                obs.obs_sceneitem_set_visible(item, visible)
                obs.obs_source_set_enabled(src, not disable if visible else False)
                _log(obs.LOG_INFO, f"Scene '{scene_name}': {'show' if visible else 'hide'} '{source_name}' (disable={disable})")
                return True
            sub_scene = None
            if obs.obs_source_is_group(src):
                sub_scene = obs.obs_group_from_source(src)
            elif obs.obs_source_get_type(src) == obs.OBS_SOURCE_TYPE_SCENE:
                sub_scene = obs.obs_scene_from_source(src)
            if sub_scene is not None:
                if _set_sceneitem_visibility_recursive(sub_scene, scene_name, source_name, visible, disable):
                    return True
    finally:
        obs.sceneitem_list_release(items)
    return False


def set_sceneitem_visibility(scene, scene_name, source_name, visible, disable=False):
    action = "show" if visible else "hide"
    if scene is None or not source_name:
        _log(obs.LOG_WARNING, f"Cannot {action} '{source_name}' in scene '{scene_name}' (invalid scene/name)")
        return False
    if _set_sceneitem_visibility_recursive(scene, scene_name, source_name, visible, disable):
        return True
    #_log(obs.LOG_WARNING, f"Scene '{scene_name}': source '{source_name}' not found (including groups)")
    return False


def advss_get_variable_value(name):
    proc = obs.obs_get_proc_handler()
    data = obs.calldata_create()
    obs.calldata_set_string(data, "name", name)
    obs.proc_handler_call(proc, "advss_get_variable_value", data)
    success = obs.calldata_bool(data, "success")
    value = obs.calldata_string(data, "value") if success else None
    obs.calldata_destroy(data)
    return value


def advss_set_variable_value(name, value):
    proc = obs.obs_get_proc_handler()
    data = obs.calldata_create()
    obs.calldata_set_string(data, "name", name)
    obs.calldata_set_string(data, "value", value)
    obs.proc_handler_call(proc, "advss_set_variable_value", data)
    success = obs.calldata_bool(data, "success")
    obs.calldata_destroy(data)
    if not success:
        _log(obs.LOG_WARNING, f"Could not set ADVSS variable '{name}' to '{value}'")
    return success


def rotate_once():
    raw_value = advss_get_variable_value(ROTATION_SOURCES_VAR)
    if not raw_value:
        _log(obs.LOG_WARNING, f"ADVSS variable '{ROTATION_SOURCES_VAR}' is empty")
        return False

    names = parse_source_list(raw_value)
    if not names:
        _log(obs.LOG_WARNING, f"No source names parsed from '{ROTATION_SOURCES_VAR}'")
        return False

    idx_str = advss_get_variable_value(ROTATION_INDEX_VAR)
    try:
        current_index = int(idx_str) if idx_str not in (None, "") else -1
    except Exception:
        current_index = -1

    next_index = find_next_valid_index(names, current_index)
    if next_index is None:
        _log(obs.LOG_WARNING, "No valid sources with non-zero size found")
        return False

    previous_name = names[current_index] if 0 <= current_index < len(names) else None
    next_name = names[next_index]
    _log(obs.LOG_INFO, f"Rotating: '{previous_name}' -> '{next_name}' (index {next_index})")

    scene_source = obs.obs_frontend_get_current_scene()
    if scene_source is None:
        _log(obs.LOG_WARNING, "Current scene unavailable")
        return False

    try:
        scene_name = obs.obs_source_get_name(scene_source)
        scene = obs.obs_scene_from_source(scene_source)
        if scene is None:
            _log(obs.LOG_WARNING, "Active source is not a scene")
            return False

        # First try to hide/disable the previous source in the current scene.
        if previous_name:
            if not set_sceneitem_visibility(scene, scene_name, previous_name, visible=False, disable=True):
                # Fallback: attempt to find the source in the configured fallback scene
                fallback_scene_name = advss_get_variable_value(ROTATION_FALLBACK_VAR)
                if fallback_scene_name:
                    fb_src = obs.obs_get_source_by_name(fallback_scene_name)
                    if fb_src is not None:
                        try:
                            fb_scene = obs.obs_scene_from_source(fb_src)
                            if fb_scene is not None:
                                if set_sceneitem_visibility(fb_scene, fallback_scene_name, previous_name, visible=False, disable=True):
                                    _log(obs.LOG_INFO, f"Hidden previous source '{previous_name}' in fallback scene '{fallback_scene_name}'")
                                else:
                                    _log(obs.LOG_DEBUG, f"Previous source '{previous_name}' not found in fallback scene '{fallback_scene_name}'")
                        finally:
                            obs.obs_source_release(fb_src)
                else:
                    _log(obs.LOG_DEBUG, f"Previous source '{previous_name}' not present in current scene and no fallback scene configured")

        # Try to show/enable the next source in the current scene.
        if not set_sceneitem_visibility(scene, scene_name, next_name, visible=True, disable=False):
            # Fallback: try to find and show the source in the configured fallback scene
            fallback_scene_name = advss_get_variable_value(ROTATION_FALLBACK_VAR)
            if fallback_scene_name:
                fb_src = obs.obs_get_source_by_name(fallback_scene_name)
                if fb_src is not None:
                    try:
                        fb_scene = obs.obs_scene_from_source(fb_src)
                        if fb_scene is not None and set_sceneitem_visibility(fb_scene, fallback_scene_name, next_name, visible=True, disable=False):
                            _log(obs.LOG_INFO, f"Enabled source '{next_name}' in fallback scene '{fallback_scene_name}'")
                        else:
                            _log(obs.LOG_WARNING, f"New source '{next_name}' missing from scene '{scene_name}' and not found in fallback scene '{fallback_scene_name}'")
                            return False
                    finally:
                        obs.obs_source_release(fb_src)
                else:
                    _log(obs.LOG_WARNING, f"Fallback scene '{fallback_scene_name}' not found when looking for '{next_name}'")
                    return False
            else:
                _log(obs.LOG_WARNING, f"New source '{next_name}' missing from scene '{scene_name}' and no fallback scene configured")
                return False
    finally:
        obs.obs_source_release(scene_source)

    advss_set_variable_value(ROTATION_INDEX_VAR, str(next_index))
    advss_set_variable_value(ROTATION_RUNNING_VAR, "1")
    _log(obs.LOG_INFO, f"Rotation complete -> '{next_name}' (index {next_index})")
    return True


def run():
    """Entry point AdvSS expects for inline scripts."""
    _log(obs.LOG_INFO, "run()")
    return rotate_once()
