from models.corridor import Corridor
from text import epilogue, intro, run_corridor


def main():
    corridor = Corridor()

    with open("book/001-intro.md", "w") as intro_file:
        intro_file.write("## Introduction\n\n")
        intro_file.write(intro(corridor))

    with open("book/002-corridor.md", "w") as corridor_file:
        corridor_file.write("## The corridor\n\n")
        corridor_file.write(corridor.get_history())

    messages = run_corridor(corridor)
    for chapter, run_messages in messages.items():
        number = str(chapter + 2).zfill(3)
        with open(f"book/{number}-run.md", "w") as run_file:
            for m in run_messages:
                run_file.write(m + "\n\n")

    number = chapter + 3
    with open(f"book/{str(number).zfill(3)}-epilogue.md", "w") as epilogue_file:
        epilogue_file.write("## Epilogue\n\n")
        epilogue_file.write(epilogue(corridor) + "\n\n")

    number += 1
    with open(f"book/{str(number).zfill(3)}-appendix.md", "w") as appendix_file:
        appendix_file.write("## Appendix\n")
        for s in corridor.stats():
            appendix_file.write(s + "\n")


if __name__ == "__main__":
    main()
