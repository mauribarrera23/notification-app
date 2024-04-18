# Generate secret key
    openssl rand -hex 32

# Run unit tests
    pytest --disable-pytest-warnings .


#
    docker run --tty --network notifications-app_default confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=s -s value=avro -r http://schema-registry:8085 -t postgres.public.notification
