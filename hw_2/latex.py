import os
import subprocess
from typing import Iterator, Optional, Callable, TypeVar


def array_to_elements_generator(data: list):
    yield len(data)
    for i in data:
        # yield len(i)
        for j in i:
            yield j


a = TypeVar('a')


def maybe_place(x: Optional[a], f: Callable[[a], str]):
    return f(x) if x is not None else ''


def latex_generating_func(header: str, picture: Optional[str], generator: Iterator, data: list):
    def place_picture_if_any(x: str):
        return '\n'.join(["\\subsection{Картинка}", f"\\includegraphics[scale=0.25]{{{x}}}"])

    def max_length():
        return max(map(len, data))

    def content(begin: str, end: str, rows: int, max_len: int):
        def inner_content():
            def line():
                return " & ".join([str(next(generator)) for _ in range(max_len)])

            return " \\\\ \n".join([line() for _ in range(rows)]) + " \\\\"

        return '\n'.join([begin, inner_content(), end])

    def beginning(begin: str, end: str, rows: int):
        def wrap_start(repeat_count: int):
            def wrap_repeatable_holder():
                return ' '.join('c' * repeat_count)

            return '\n'.join([header, begin, f"\\begin{{tabular}}{' '.join(['{', wrap_repeatable_holder(), '}'])}"])

        def wrap_end():
            return '\n'.join(["\\end{tabular}", "\\end{center}", maybe_place(picture, place_picture_if_any), end])

        return content(wrap_start(max_length()), wrap_end(), rows, max_length())

    return beginning("\\begin{center}", end="\n".join(["\\end{document}"]), rows=next(generator))


def generate_tex(data: list, image: Optional[str]):
    return latex_generating_func(
        "\n".join(["\\documentclass{article}", "\\usepackage[russian]{babel}", "\\usepackage{graphicx}",
                   "\\begin{document}", "\\section{Сводный отчет}", "\\subsection{Таблица}"]),
        picture=image,
        generator=array_to_elements_generator(data), data=data)


def save_as_tex(data: str, should_generate: Optional[bool]):
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/summary.tex", "w", encoding="UTF-8") as text_file:
        text_file.write(data)
    maybe_place(should_generate, lambda x: os.system('pdflatex -output-directory artifacts artifacts/summary.tex'))
    # os.system("pdflatex artifacts/summary.tex")

