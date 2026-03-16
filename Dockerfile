# base image
FROM python:3.10

# working directory
WORKDIR /app

# copy requirements
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy dataset files
COPY ./data/collab_filtered_data.csv \
     ./data/interaction_matrix.npz \
     ./data/track_ids.npy \
     ./data/cleaned_data.csv \
     ./data/transformed_data.npz \
     ./data/transformed_hybrid_data.npz \
     ./data/

# copy python files
COPY app.py \
     collaborative_filtering.py \
     content_based_filtering.py \
     hybrid_recommendations.py \
     data_cleaning.py \
     transform_filtered_data.py \
     ./

# expose port
EXPOSE 8000

# start application
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]