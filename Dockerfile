FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt

ADD bot.py /
ADD command_list.yaml /
ADD cogs/ cogs/


CMD [ "python", "bot.py"]