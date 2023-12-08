from dataclasses import dataclass

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Mm, Cm
from docx.shared import Pt
from docx.enum.section import WD_ORIENT


@dataclass
class TableReport:
    col_names: list | tuple
    data: list | tuple
    report_name: str


def generate_report(tables: list[TableReport], doc_info):
    # создание документа
    doc = Document()
    # доступ к первой секции:
    section = doc.sections[0]
    # высота листа в сантиметрах
    section.page_height = Cm(25)
    # ширина листа в сантиметрах
    section.page_width = Cm(30.0)
    section.left_margin = Mm(20.4)
    section.right_margin = Mm(10)
    section.top_margin = Mm(15)
    section.bottom_margin = Mm(10)
    section.header_distance = Mm(10)
    section.footer_distance = Mm(10)

    # Заголовок
    title = doc.add_heading('Отчёт', level=1)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    for run in title.runs:
        run.font.size = Pt(20)
    title = doc.add_heading(f"за период {doc_info['start_data']} - {doc_info['end_data']}", level=1)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    for run in title.runs:
        run.font.size = Pt(15)

    for table in tables:
        doc.add_paragraph(" ")
        doc.add_heading(table.report_name, level=2)
        # создание таблицы
        table_total = doc.add_table(rows=len(table.data) + 1, cols=len(table.col_names))
        table_total.style = 'Light Shading Accent 1'

        #заполнение названий столбцов
        for i in range(len(table.col_names)):
            cell = table_total.cell(0, i)
            cell.paragraphs[0].add_run(table.col_names[i]).bold = True

        sum_of_types = {}
        # заполнение данными
        num_of_row = 1

        for elem in table.data:
            num_of_col = 0
            for key, value in elem.items():
                cell = table_total.cell(num_of_row, num_of_col)
                cell.text = str(value)
                num_of_col += 1
            num_of_row += 1

    empty_space = doc.add_paragraph(" ")

    paragraph = doc.add_paragraph()
    run = paragraph.add_run(f"Подготовил    {doc_info['signature']}")
    font = run.font
    font.size = Pt(15)
    filename = "report.docx"
    doc.save(filename)
    return filename


names_of_col = ["Продукт", "Тип операции", "Дата", "Склад", "Количество", "Единица измерения", "Цена за единицу", "Сумма"]

data_tuple = (
    {
        "type": "песок",
        "type_of_operation": "добыча",
        "data": "2023-11-01",
        "stock": "карьер №1",
        "count": 500,
        "unit": "тонн",
        "price": 1000,
        "sum": 500000
    },
    {
        "type": "глина",
        "type_of_operation": "добыча",
        "data": "2023-11-03",
        "stock": "карьер №2",
        "count": 300,
        "unit": "тонн",
        "price": 800,
        "sum": 240000
    },
    {
        "type": "песок",
        "type_of_operation": "продажа",
        "data": "2023-11-05",
        "stock": "потребитель №1",
        "count": 400,
        "unit": "тонн",
        "price": 2000,
        "sum": 800000
    },
    {
        "type": "глина",
        "type_of_operation": "продажа",
        "data": "2023-11-07",
        "stock": "потребитель №2",
        "count": 200,
        "unit": "тонн",
        "price": 1500,
        "sum": 300000
    },
    {
        "type": "песок",
        "type_of_operation": "продажа",
        "data": "2023-11-20",
        "stock": "потребитель №3",
        "count": 600,
        "unit": "тонн",
        "price": 2500,
        "sum": 1500000
    }
)

doc_info = {"start_data": '12.12.2021',
            "end_data": '12.12.2022',
            "signature": "Иванов"}

if __name__ == '__main__':
    generate_report(len(data_tuple), len(names_of_col), names_of_col, data_tuple, doc_info)
