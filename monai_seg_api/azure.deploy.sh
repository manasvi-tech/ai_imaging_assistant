#!/bin/bash

RESOURCE_GROUP="monai-api-rg"
ACR_NAME="monairegistry"
IMAGE_NAME="monai-seg-api"
CONTAINER_NAME="monai-container"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location eastus

# Create ACR
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Login and push Docker image
az acr login --name $ACR_NAME
az acr build --registry $ACR_NAME --image $IMAGE_NAME .

# Deploy container instance with GPU
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_NAME.azurecr.io/$IMAGE_NAME \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $(az acr credential show -n $ACR_NAME --query "username" -o tsv) \
  --registry-password $(az acr credential show -n $ACR_NAME --query "passwords[0].value" -o tsv) \
  --cpu 4 \
  --memory 16 \
  --gpu-count 1 \
  --gpu-sku K80 \
  --ports 8000 \
  --dns-name-label monai-seg-api
