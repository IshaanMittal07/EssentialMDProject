FROM python:3.9-slim

WORKDIR / app 

# Install the dependencies
COPY src/requirements.txt /app/requirements.txt 
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the parser 
COPY src/metadata_parser.py /app/metadata_parser.py 

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh 

CMD ["/app/entrypoint.sh"]

#References: 
#https://kinsta.com/blog/dockerfile-entrypoint/