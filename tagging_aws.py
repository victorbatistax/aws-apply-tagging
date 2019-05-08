import boto3
import pandas as pd
from termcolor import colored


# Here make use the API boto3 for work tagging resource.
ec2 = boto3.resource('ec2',region_name='us-east-1')
client = boto3.client('ec2', region_name='us-east-1')

# read a csv file and do use collumn with dataset. 
df = pd.read_csv('TagEc2Virginia.csv', delimiter=';')
df = pd.read_csv('TagsRCI_SP.csv', delimiter=';')
AllInstances = []

for i in range(len(df)):
	if df['Region'][i] == 'sa-east-1' and df['Resource type'][i] == 'EC2 Instance':
		AllInstances.append(df['ID'][i])
        #print("Region: {0}\tId: {1}\tProjeto: {2}\tAmbiente: {3}\tEmpresa: {4}\tPais: {5}".format(df['Region'][i], df['ID'][i], df['Projeto'][i], df['Ambiente'][i], df['Empresa'][i], df['Pais'][i]))


#Adiciona Chave e Valor a Intancias Ec2
for idx in range(len(AllInstances)):
    response = client.create_tags(
        Resources=[df['ID'][idx]],
        Tags=[
            {
                'Key': 'Projeto',
                'Value': df['Projeto'][idx]
            },
            {   'Key': 'Ambiente',
                'Value': df['Ambiente'][idx]
            },
            {
                'Key': 'Empresa',
                'Value': df['Empresa'][idx]
            },
            {
                'Key': 'Pais',
                'Value': df['Pais'][idx]
            }          
        ]
    )



MARCAS = ["Ambiente", "Projeto", "Pais", "Empresa"]

response = client.describe_snapshots(OwnerIds=['idx_owner'])
snapshot_list=response['Snapshots']

# Get the markers of ec2 instances and replicate for all services attacheds
instances = boto3.resource('ec2', region_name='sa-east-1').instances.all()
for instance in instances:
    tags = [t for t in instance.tags or [] if t['Key'] in MARCAS]
    if not tags:
        continue

    # Tag EBS Volumes
    for vol in instance.volumes.all():
        print('Atualizando {}'.format(vol.id))
        vol.create_tags(Tags=tags)

    # Tag EIP's
    
    # Tag ENI
    for eni in instance.network_interfaces:
        print('Atualizando {}'.format(eni.id))
        eni.create_tags(Tags=tags)

    # Tag Snapshot
    for i in range(len(snapshot_list)):
        for vol in instance.volumes.all():
            if vol.id == snapshot_list[i]['VolumeId']:
                snapshot = ec2.Snapshot(snapshot_list[i]['SnapshotId'])
                print(snapshot, " ====> ", vol.id)
                snapshot.create_tags(Tags=tags)

    for i in range(len(snapshot_list)):
        for vol in instance.volumes.all():
            if vol.id == snapshot_list[i]['VolumeId']:
                snapshot = ec2.Snapshot(snapshot_list[i]['SnapshotId'])
                print(snapshot, " ====> ", vol.id)
                snapshot.create_tags(Tags=tags)
                print(colored('CREATED', 'red'))
    


#response = image.describe_attribute()
