import xlsxwriter
from sqlalchemy import create_engine, Column, BigInteger, VARCHAR, JSON, func, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_PREFIX_URI = ""
SQLALCHEMY_DATABASE_DB_NAME = "prod_db"


engine = create_engine(SQLALCHEMY_DATABASE_PREFIX_URI)

Base = declarative_base()


class TaskResult(Base):
    __tablename__ = "task_result"
    id = Column(BigInteger, nullable=False, primary_key=True)
    result = Column(JSON, nullable=False)
    task_name = Column(VARCHAR(), nullable=False)
    linked_task = Column(VARCHAR())
    success_result = Column(JSON)
    error_result = Column(JSON)
    task_date = Column(DateTime, server_default=func.now())
    completed = Column(Boolean())
    task_id = Column(VARCHAR())


def prepare_data_for_table(data, success_result=None, start_row=0):
    res = []
    row = start_row
    data_elements = range(len(data)) if isinstance(data, list) else data
    for element in data_elements:
        for key, value in data[element].items():
            if success_result is not None:
                temp = [i[1] for i in success_result if key == i[0]]
                el = temp[0] if len(temp) > 0 else ''
            else:
                el = element
            res.append((row, 0, el))
            res.append((row, 1, key))
            res.append((row, 2, value))
            row += 1
    return res


Session = sessionmaker(engine)
with Session() as session:
    task_result_create = (
        session  # replace
        .query(TaskResult)
        .filter(TaskResult.task_name == "create_bill")
        .order_by(TaskResult.id.asc())
        .first()
    )

    create_count = task_result_create.result.get('customer_count')
    create_error = task_result_create.error_result
    create_success = [(t['bill'].get('number'), t['agent'].get('login')) for t in task_result_create.success_result]

    print(create_error)

    create_error_cells = prepare_data_for_table(create_error, start_row=1)
    print(create_error_cells)

    task_result_sent = (
        session
        .query(TaskResult)
        .filter(TaskResult.task_name == "send_bill_mail")
        .order_by(TaskResult.id.asc())
        .first()
    )

    sent_error = task_result_sent.error_result

    print(sent_error)

    sent_error_cells = prepare_data_for_table(sent_error, create_success, start_row=1)
    print(sent_error_cells)

    # for i in range(2, len(sent_error_cells), 3):
    #     for j in create_success:
    #         if sent_error_cells[i-1][2]

    workbook = xlsxwriter.Workbook('t.xslx')
    bold = workbook.add_format({'bold': True})

    worksheet_create = workbook.add_worksheet('Ошибки создания')
    worksheet_create.write(1, 0, 'Название группы ошибок', bold)
    worksheet_create.write(1, 1, 'Клиент', bold)
    worksheet_create.write(1, 2, 'Ошибка', bold)
    worksheet_create.set_column(0, 1, 25)
    worksheet_create.set_column(2, 2, 50)

    worksheet_sent = workbook.add_worksheet('Ошибки отправки')
    worksheet_sent.write(0, 0, 'Клиент', bold)
    worksheet_sent.write(0, 1, 'Счет', bold)
    worksheet_sent.write(0, 2, 'Ошибка', bold)
    worksheet_sent.set_column(0, 1, 25)
    worksheet_sent.set_column(2, 2, 50)

    [worksheet_create.write(*cell) for cell in create_error_cells]
    [worksheet_sent.write(*cell) for cell in sent_error_cells]
    workbook.set_tab_ratio(75)
    workbook.close()

    # print(create_count)
    # print(create_error)
    # print(sent_error)
