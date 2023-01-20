#!/bin/bash

#This script deploys the packaged module to Synapse Analytics Workspace.
#The wheel package is copied to the libraries folder of the sqlpool in synapse data lake
#The config file is copied to the config folder in landing container
#The definition python file is copied to the definitions folder in landing container

#Authenticate with Azure using Service Principal
az login --service-principal -u $serviceuser --password="$servicesecret" --tenant $servicetenant

#Copy Definition File to Landing Container
DEFINITION_FILE=$definitionfile
DEFINITION_FILE_TARGET=$definitionfiletarget
LANDING_SA=$landingaccount
LANDING_FS=$landingcontainer
az storage fs file upload \
		-s ${DEFINITION_FILE} \
		-p ${DEFINITION_FILE_TARGET} \
		-f ${LANDING_FS} \
		--account-name ${LANDING_SA} \
		--auth-mode login \
		--overwrite

#Copy Config File to Landing Container
CONFIG_FILE=$configfile
CONFIG_FILE_TARGET=$configfiletarget
LANDING_SA=$landingaccount
LANDING_FS=$landingcontainer
az storage fs file upload \
		-s ${CONFIG_FILE} \
		-p ${CONFIG_FILE_TARGET} \
		-f ${LANDING_FS} \
		--account-name ${LANDING_SA} \
		--auth-mode login \
		--overwrite

#Install Package Wheel File into Azure Synapse
WHEEL_NAME=dist/$packagename-1.0.0-py3-none-any.whl

WP_PACKAGE=$(az synapse workspace-package show --workspace-name $workspacename --name $packagename-1.0.0-py3-none-any.whl)
if [[ $WP_PACKAGE = *[!\ ]* ]]; then
  echo "Job already exists, it will be deleted from pool and workspace"
  az synapse spark pool update --name $sparkpool --workspace-name $workspacename --resource-group $rgname --package-action Remove --package $packagename-1.0.0-py3-none-any.whl
  az synapse workspace-package delete --workspace-name $workspacename --name $packagename-1.0.0-py3-none-any.whl --yes
else
  echo "Job does not exists, the delete is skipped"
fi

az synapse workspace-package upload --workspace-name $workspacename --package ${WHEEL_NAME}
az synapse spark pool update --name $sparkpool --workspace-name $workspacename --resource-group $rgname --package-action Add --package $packagename-1.0.0-py3-none-any.whl