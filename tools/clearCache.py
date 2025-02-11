import os
import shutil

if os.path.isdir("__pycache__"):
    shutil.rmtree(os.path.join("__pycache__"))

if os.path.isdir("taskman_backend/__pycache__"):
    shutil.rmtree(os.path.join("taskman_backend/__pycache__"))

if os.path.isdir("taskman_backend/migrations/__pycache__"):
    shutil.rmtree(os.path.join("taskman_backend/migrations/__pycache__"))

if os.path.isdir("taskman_backend/models/__pycache__"):
    shutil.rmtree(os.path.join("taskman_backend/models/__pycache__"))

if os.path.isdir("taskman_backend/serializers/__pycache__"):
    shutil.rmtree(os.path.join("taskman_backend/serializers/__pycache__"))

if os.path.isdir("taskman_backend/static/media/data/__pycache__"):
    shutil.rmtree(os.path.join("taskman_backend/static/media/data/__pycache__"))

if os.path.isdir("taskman_backend/views/__pycache__"):
    shutil.rmtree(os.path.join("taskman_backend/views/__pycache__"))

if os.path.isdir("tools/__pycache__"):
    shutil.rmtree(os.path.join("tools/__pycache__"))