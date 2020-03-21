FROM nginx as base

RUN apt update \
	&& apt install -y locales

# Uncomment en_US.UTF-8 for inclusion in generation
RUN sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen
RUN echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen

# Generate locale
RUN locale-gen

# Export env vars
RUN echo "export LC_ALL=zh_CN.UTF-8" >> ~/.bashrc
RUN echo "export LANG=en_US.UTF-8" >> ~/.bashrc
RUN echo "export LANGUAGE=en_US.UTF-8" >> ~/.bashrc

RUN apt install -y fonts-noto fonts-noto-cjk

FROM base

COPY default.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html
