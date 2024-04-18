FROM confluentinc/cp-kafkacat

WORKDIR /src

COPY ./compose/local/backend/kafka-consumer/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
