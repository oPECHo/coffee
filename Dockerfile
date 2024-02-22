FROM debian:sid
# RUN echo 'deb http://mirrors.psu.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ stable main contrib non-free' >> /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ experimental main contrib non-free' >> /etc/apt/sources.list
RUN apt update --fix-missing && apt dist-upgrade -y
RUN apt install -y python3 python3-dev python3-pip python3-venv git locales ca-certificates curl gnupg
RUN apt install -y -t experimental npm
RUN sed -i '/th_TH.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG th_TH.UTF-8 
ENV LANGUAGE th_TH:en 
# ENV LC_ALL th_TH.UTF-8

#RUN echo 'curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/nodesource.gpg'

RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python3
RUN $PYTHON -m pip install wheel poetry gunicorn

WORKDIR /app
# COPY fonts /app/fonts
# RUN mkdir -p /usr/share/fonts/opentype && cp -r fonts/* /usr/share/fonts/opentype/ && fc-cache -fv

COPY coffee/cmd /app/coffee/cmd
COPY poetry.lock pyproject.toml /app/
RUN $PYTHON -m poetry config virtualenvs.create false && $PYTHON -m poetry install --no-interaction --only main

COPY coffee/web/static/package.json coffee/web/static/package-lock.json coffee/web/static/
RUN npm install --prefix coffee/web/static

COPY . /app
ENV COFFEE_SETTINGS=/app/coffee-production.cfg

# For brython
# RUN cd /app/kampan/web/static/brython; \
#     for i in $(ls -d */); \
#     do \
#     cd $i; \
#     python3 -m brython --make_package ${i%%/}; \
#     mv *.brython.js ..; \
#     cd ..; \
#     done
