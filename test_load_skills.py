import os
import sys
from core.registry import SkillRegistry

def test_load():
    registry = SkillRegistry()
    skills_dir = os.path.join(os.getcwd(), "features")
    print(f"Loading from: {skills_dir}")
    registry.load_skills(skills_dir)
    print("\nLOADED SKILLS:")
    for name in registry.skills:
        print(f" - {name}")
    print("\nAVAILABLE TOOLS:")
    for tool in registry.tools_schema:
        print(f" - {tool['function']['name']}")

if __name__ == "__main__":
    test_load()
