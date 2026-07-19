from agent.llm import chat_json


def generate_script(idea: dict, genome) -> dict:
    """
    Returns {"scenes": [{"narration": str, "image_prompt": str}, ...]}
    Scene count and system prompt come from the active genome, so this
    changes as the genome evolves.
    """
    n_scenes = genome.scene_count_shorts if idea["format"] == "shorts" else genome.scene_count_long
    length_note = genome.length_note_shorts if idea["format"] == "shorts" else genome.length_note_long

    result = chat_json(
        system=genome.script_system_prompt,
        user=(
            f"Title: {idea['title']}\n"
            f"Hook: {idea['hook']}\n"
            f"Outline: {idea['outline']}\n"
            f"Generate exactly {n_scenes} scenes covering this outline in order. "
            f"Keep total narration length appropriate for {length_note}."
        ),
        temperature=0.7,
    )
    return result


def generate_seo_metadata(idea: dict, script: dict, genome) -> dict:
    """Returns {title, description, tags[]}"""
    return chat_json(
        system=genome.seo_system_prompt,
        user=f"Video title idea: {idea['title']}\nScenes: {[s['narration'] for s in script['scenes']]}",
        temperature=0.5,
    )
