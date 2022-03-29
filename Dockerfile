FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV=dev
CMD python -m python -s --alluredir=test_results/ /tests_project/tests/