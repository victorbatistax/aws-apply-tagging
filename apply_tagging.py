import boto3
s3 = boto3.resource('s3')


regions = ['ap-south-1','eu-west-3','eu-west-2','eu-west-1','ap-northeast-3','ap-northeast-2','ap-northeast-1',
			'sa-east-1','ca-central-1','ap-southeast-1','ap-southeast-2','eu-central-1','us-east-1','us-east-2','us-west-1','us-west-2']

def apply_tagging_mul_regions():
    for region in regions:
        resource_tagging(regionn=region)


def AmazonRDS(regionn ='us-east-1'):
    '''Apply Tag in RDS resource'''

    client = boto3.client('rds', region_name = regionn)
    # Get the all arn of DBInstances
    db_arn = []
    db_instances = client.describe_db_instances()
    for db in db_instances['DBInstances']:
        db_arn.append(db['DBInstanceArn'])

    # Set Tags
    for arn in db_arn:
        response = client.add_tags_to_resource(
            ResourceName = arn,
            Tags = [
                {
                    'Key': 'teste1',
                    'Value': 'stag'
                },
            ]
        )


def AWSCertificateManager(regionn ='us-east-1'):
	client = boto3.client('acm', region_name = regionn)
	
	list_acm = client.list_certificates()

	for arn in list_acm['CertificateSummaryList']:
		response = client.add_tags_to_certificate(
    		CertificateArn=arn['CertificateArn'],
    		Tags=[
    		    {
    		        'Key': 'Test',
    		        'Value': 'stg'
    		    },
    	])


	for arn in list_acm['CertificateSummaryList']:
		response = client.list_tags_for_certificate(
    		CertificateArn=arn['CertificateArn']
		)
		print(response, end='\n')	


def AmazonCloudFront(regionn ='us-east-1'):
	...


def AWSCloudTrail(regionn ='us-east-1'):
	client = boto3.client('cloudtrail', region_name = regionn)

	list_cloudtrail = client.describe_trails()

	for arn in list_cloudtrail['trailList']:
		response = client.add_tags(
	    ResourceId=arn['TrailARN'],
	    	TagsList=[
	    	    {
	    	        'Key': 'Test',
	    	        'Value': 'stg'
	    	    },
	    	]
		)
	
	for arn in list_cloudtrail['trailList']:
		response = client.list_tags(
    		ResourceIdList=[arn['TrailARN']]
    	)
		print(response, end='\n')


def AmazonCloudWatchLogs(regionn ='us-east-1'):
	...

def AmazonDynamoDB(regionn ='us-east-1'):
	...

def AmazonEBS(regionn ='us-east-1'):
	ec2 = boto3.resource('ec2', region_name = regionn)

	for instance in ec2.instances.all():
		for volume in instance.volumes.all():
			volume.create_tags(
        	Tags=[
        	{
        	    'Key': 'string',
            	'Value': 'string'
			}
    	]
		)


def AmazonEC2(regionn ='us-east-1'):
	client = boto3.client('ec2', region_name=regionn)
	ec2 = boto3.resource('ec2', region_name=regionn)

	filters = [{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}]

	# filter the instances based on filters() above
	instances = ec2.instances.filter(Filters=filters)

	# instantiate empty array
	AllInstances = []

	for instance in instances:
		# for each instance, append to array and print instance id
		AllInstances.append(instance.id)
		#print instance.id
		response = client.create_tags(
		    Resources=AllInstances,
		    Tags=[
		        {
		            'Key': 'teste1',
		            'Value': 'victor Stag',
		        },
		    ]
		)


def AWSElasticBeanstalk(regionn ='us-east-1'):
	client = boto3.client('elasticbeanstalk')

	list_anr_env = client.describe_environments()

	for arn in list_anr_env['Environments']:
		client.update_tags_for_resource(
	    ResourceArn=arn['EnvironmentArn'],
	    TagsToAdd=[
	        {
	            'Key': 'teste1',
	            'Value': 'stg'
	        }
	    ])

	for arn in list_anr_env['Environments']:
		response = client.list_tags_for_resource(
    		ResourceArn=arn['EnvironmentArn']
		)
		print(response, end='\n')


def AmazonElasticFileSystem(regionn ='us-east-1'):
	client = boto3.client('efs', region_name = regionn)

	list_fs_id = client.describe_file_systems()

	for fsid in list_fs_id['FileSystems']:
		response = client.create_tags(
    		FileSystemId=fsid['FileSystemId'],
    		Tags=[
    		    {
    		        'Key': 'Test',
    		        'Value': 'stg'
    		    },
    		]
		)
		response = client.describe_tags(FileSystemId=fsid['FileSystemId'])
		print(response, end='\n')


def ElasticLoadBalancing(regionn ='us-east-1'):
	client = boto3.client('elb', region_name = regionn)

	list_elb_names = client.describe_load_balancers()


	for name in list_elb_names['LoadBalancerDescriptions']:
		response = client.add_tags(
	    	LoadBalancerNames=[
	    	    name['LoadBalancerName']
	    	],
	    	Tags=[
	    	    {
	    	        'Key': 'Test',
	    	        'Value': 'stg'
	    	    },
	    	]
		)

	for name in list_elb_names['LoadBalancerDescriptions']:
		response = client.describe_tags(
    		LoadBalancerNames=[
    		    name['LoadBalancerName']
    		]
		)
		print(response, end='\n')


def ElasticLoadBalancingV2(regionn ='us-east-1'):
	client = boto3.client('elbv2', region_name = regionn)

	list_elb_names = client.describe_load_balancers()


	for arn in list_elb_names['LoadBalancers']:
		response = client.add_tags(
	    	ResourceArns = [arn['LoadBalancerArn']],
	    	Tags=[
	    	    {
	    	        'Key': 'Test',
	    	        'Value': 'stg'
	    	    }
	    	]
		)

	for arn in list_elb_names['LoadBalancers']:
		response = client.describe_tags(
    		ResourceArns=[
    		    arn['LoadBalancerArn']
    		]
		)
		print(response, end='\n')


def AmazonElastiCache(regionn ='us-east-1'):
	client = boto3.client('elasticcache', region_name=regionn)
	response = client.describe_cache_clusters()
	
	response = client.add_tags_to_resource(
    ResourceName='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        }
    ]
	)

def AmazonElasticsearchService(regionn ='us-east-1'):
	...

def AmazonGlacier(regionn ='us-east-1'):
	...

def AWSLambda(regionn ='us-east-1'):
	client = boto3.client('lambda', region_name = regionn)

	list_fun = client.list_functions()

	for arn in list_fun['Functions']:
		client.tag_resource(
    		Resource=arn['FunctionArn'],
    		Tags={
    		    'test': 'stag'
    		})

	for arn in list_fun['Functions']:
		print(client.list_tags( 
    	    Resource=arn['FunctionArn'] 
    	))   		

def AmazonRedshift(regionn ='us-east-1'):
	...

def AmazonRoute53():
	client = boto3.client('route53')
	
	hostedZone = client.list_hosted_zones_by_name()

	for resourceId in hostedZone['HostedZones']:
		r_id = resourceId['Id'].replace('/hostedzone/', '')
		response = client.change_tags_for_resource(
    		ResourceType = 'hostedzone',
    		ResourceId = r_id,
    		AddTags = [
    	    {
    	        'Key': 'Ultima2',
    	        'Value': 'Verificao2'
    	    }]
		)

	for resourceId in hostedZone['HostedZones']:
		r_id = resourceId['Id'].replace('/hostedzone/', '')
		response = client.list_tags_for_resource( 
    	    ResourceType='hostedzone', 
    	    ResourceId=r_id 
    	) 	
		print(response['ResourceTagSet'], end='\n')

def AmazonS3():
    client = boto3.client('s3')
    #s3 = boto3.resource('s3')

    list_buckets = client.list_buckets()
    lnb = []

    for bn in list_buckets['Buckets']:
        lnb.append(bn['Name'])
        # bucket_tagging = s3.BucketTagging(bn['Name'])
        # bucket_tagging

    for name in lnb:
        print(name)
        Tagg = {'TagSet': [
            {'Key': 'Teste', 'Value': 'StagTag'},
            {'Key': 'Teste2', 'Value': 'StagTagUnique'}
        ]}
        lista1 = Tagg['TagSet']

        try:
            tag = client.get_bucket_tagging(Bucket=name)
            lista = tag['TagSet']
            if not tag['TagSet'] == Tagg['TagSet']:
                for el in lista1:
                    for ell in lista:
                    	if el == ell:
                    		lista.remove(ell)

                lista.exestend(lista1)

            Tagg['TagSet'] = lista
            print(Tagg)
            # client.put_bucket_tagging(
            # Bucket = name,
            # Tagging = Tagg
            # )
        except Exception:
            client.put_bucket_tagging(
                Bucket=name,
                Tagging=Tagg
            )
        else:
            print('Deu ruim')


def AmazonSageMaker(regionn ='us-east-1'):
	...

def AmazonSimpleQueueService(regionn ='us-east-1'):
	client = boto3.client('sqs', region_name=regionn)

	queueUrls = client.list_queues()

	for url in queueUrls['QueieUrls']:
		response = client.tag_queue(
    	QueueUrl=url,
    	Tags={
    	    'string': 'string'
    	}
		)

def AmazonVPC(regionn ='us-east-1'):
	ec2 = boto3.resource('ec2')
	vpc = ec2.Vpc('id')

	tag = vpc.create_tags(
    DryRun=True,
    Tags=[
        {
            'Key': 'test',
            'Value': 'stg'
        },
    ]
	)

def resource_tagging(regionn ='us-east-1'):
    client = boto3.client('resourcegroupstaggingapi', region_name = regionn)
    # resources_map = client.get_resources()
    clientt = boto3.client('s3')
    list_buckets = clientt.list_buckets()
    
    idx =len(list_buckets['Buckets'])
    arn_list = []
    
    
    for i in range(idx):
        arn_list.append('arn:aws:s3:::'+list_buckets['Buckets'][i]['Name'])
    
    
    k = idx // 20
    q = idx % 20
    pos = 0
    for j in range(1,k+1):
        listarn = arn_list[pos:j*20]
        pos += 20
        client.tag_resources(
            ResourceARNList = listarn,
            Tags={
                'Proprietario': 'Teste'
            }
        )
        
    
    if q:
        client.tag_resources(
            ResourceARNList = arn_list[idx-q:idx],
            Tags={
                'Proprietario': 'Teste'
            }
        )