import boto3

AWS_KEY = 'AWS_KEY'
AWS_SEC_KEY = 'AWS_SEC_KEY'

client = boto3.client('route53', aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SEC_KEY)


def list_all_records():
    hosts_list = client.list_hosted_zones()
    zones = hosts_list['HostedZones']

    for zone in zones:
        if 'Name' in zone:
            print "===========ID==========|=============NAME====================="
            zname = zone['Name']
            zid = zone['Id'].replace('/hostedzone/', '')
            print "\t{zid}\t{zname}".format(zid=zid, zname=zname)
            print "=============================================================="

            a_record_list = client.list_resource_record_sets(HostedZoneId=zid)
            j=1
            for record in a_record_list['ResourceRecordSets']:
                # if record['Type'] == 'A':
                record_type = record['Type']
                record_name = record['Name']
                ttl = record['TTL']
                for entry in record['ResourceRecords']:
                    record_ip = entry['Value']
                    print "{j}\t{record_type} \t{record_name}\t{record_ip}\t{ttl}" \
                        .format(j=j, \
                                record_type=record_type, \
                                record_name=record_name, \
                                record_ip=record_ip, ttl=ttl)
                j+=1


def list_hosted_zones():
    hosts_list = client.list_hosted_zones()
    zones = hosts_list['HostedZones']

    print "|====NUM=====|=======ID========|=============NAME============|"

    i=1
    for zone in zones:
        zname = zone['Name']
        zid = zone['Id'].replace('/hostedzone/', '')
        print "\t{i}\t{zid}\t\t{zname}".format(i=i,zid=zid, zname=zname)
        i+=1


def get_zone_id(domain_name):
    print 'Looking for Zone: {domain_name}'.format(domain_name=domain_name)

    hosts_list = client.list_hosted_zones()
    zones = hosts_list['HostedZones']
    for zone in zones:
        zname = zone['Name']
        if zname == domain_name:
            zid = zone['Id'].replace('/hostedzone/', '')
            return zid


def list_records_by_id(id):
    print "=============================================================="
    print '{id} DNS records:'.format(id=id)
    print '=============================================================='

    all_records_list = client.list_resource_record_sets(HostedZoneId=id)

    j=1
    for record in all_records_list['ResourceRecordSets']:
        record_type = record['Type']
        record_name = record['Name']
        ttl = record['TTL']

        for entry in record['ResourceRecords']:
            record_ip = entry['Value']
            print "{j}\t{record_type} \t{record_name}\t{record_ip}\t{ttl}" \
                .format(j=j, \
                        record_type=record_type, \
                        record_name=record_name, \
                        record_ip=record_ip, \
                        ttl=ttl)
            j+=1


def list_health_cheks_by_zid(id):
    print '=============================================================='
    print 'Looking for HealthChecks records for : {id}'.format(id=id)
    print '=============================================================='
    all_records_list = client.list_resource_record_sets(HostedZoneId=id)

    k=1
    for record in all_records_list['ResourceRecordSets']:
        if "HealthCheckId" in record:
            health_check_name = record['Name']
            health_check_id = record['HealthCheckId']
            health_check_type = record['Type']
            health_check_failover = record['Failover']
            health_check_ttl = record['TTL']
            health_check_ident = record['SetIdentifier']

            for entry in record['ResourceRecords']:
                ip = entry['Value']
                print "{k}\t{ip}\t{health_check_name} \t{health_check_id}\t{health_check_type}\t{health_check_failover}\t{health_check_ttl}\t{health_check_ident}" \
                    .format(k=k, ip=ip, \
                            health_check_name=health_check_name, \
                            health_check_id=health_check_id, \
                            health_check_type=health_check_type, \
                            health_check_failover=health_check_failover, \
                            health_check_ttl=health_check_ttl, \
                            health_check_ident=health_check_ident)
            k+=1


def list_failovers(id):
    print '=============================================================='
    print 'Looking for FailOver records: {id}'.format(id=id)
    print "=============================================================="

    all_records_list = client.list_resource_record_sets(HostedZoneId=id)

    i=1
    for record in all_records_list['ResourceRecordSets']:
        if "Failover" in record:
            health_check_name = record['Name']
            health_check_type = record['Type']
            health_check_failover = record['Failover']
            health_check_ttl = record['TTL']
            health_check_ident = record['SetIdentifier']

            for entry in record['ResourceRecords']:
                ip = entry['Value']
                print "{i}\t{ip}\t{health_check_name}\t{health_check_type}\t{health_check_failover}\t{health_check_ttl}\t{health_check_ident}" \
                    .format(i=i, ip=ip, \
                            health_check_name=health_check_name, \
                            health_check_type=health_check_type, \
                            health_check_failover=health_check_failover, \
                            health_check_ttl=health_check_ttl, \
                            health_check_ident=health_check_ident)
            i+=1


def create_master_record(zid, domain, type, ident, ip, failover_role, ttl, healthcheck_id):
    response = client.change_resource_record_sets(
        HostedZoneId = '{zid}'.format(zid = zid),
        ChangeBatch={
            'Comment': '{domain}'.format(domain = domain),
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': '{domain}'.format(domain = domain),
                        'Type': '{type}'.format(type = type),
                        'SetIdentifier': '{ident}'.format(ident = ident),
                        'Failover': '{failover_role}'.format(failover_role = failover_role),
                        'TTL': ttl,
                        'ResourceRecords': [
                            {
                                'Value': '{ip}'.format(ip = ip)
                            },
                        ],
                        'HealthCheckId': '{healthcheck_id}'.format(healthcheck_id = healthcheck_id),
                    }
                },
            ]
        }
    )
    print("DNS record status %s "  % response['ChangeInfo']['Status'])
    print("DNS record response code %s " % response['ResponseMetadata']['HTTPStatusCode'])


def create_slave_record(zid, domain, type, ident, ip, failover_role, ttl):
    response = client.change_resource_record_sets(
        HostedZoneId = '{zid}'.format(zid = zid),
        ChangeBatch={
            'Comment': '{domain}'.format(domain = domain),
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': '{domain}'.format(domain = domain),
                        'Type': '{type}'.format(type = type),
                        'SetIdentifier': '{ident}'.format(ident = ident),
                        'Failover': '{failover_role}'.format(failover_role = failover_role),
                        'TTL': ttl,
                        'ResourceRecords': [
                            {
                                'Value': '{ip}'.format(ip = ip)
                            },
                        ]
                    }
                },
            ]
        }
    )
    print("DNS record status %s "  % response['ChangeInfo']['Status'])
    print("DNS record response code %s " % response['ResponseMetadata']['HTTPStatusCode'])


def create_healthcheck(caller_ref, master_ip, check_port, check_type, check_path, check_interval, check_failed_threshold):
    response = client.create_health_check(
        CallerReference = '{caller_ref}'.format(caller_ref = caller_ref),
        HealthCheckConfig = {
            'IPAddress': '{master_ip}'.format(master_ip = master_ip),
            'Port': check_port,
            'Type': '{check_type}'.format(check_type = check_type),
            'ResourcePath': '{check_path}'.format(check_path = check_path),
            'RequestInterval': check_interval,
            'FailureThreshold': check_failed_threshold
        }
    )
    print("Response code %s " % response['ResponseMetadata']['HTTPStatusCode'])


def get_healthchecks_id_by_ip(master_ip):
    healthcheck_checks_list = client.list_health_checks()

    if 'HealthChecks' in healthcheck_checks_list:
        for entry in healthcheck_checks_list['HealthChecks']:
            if 'HealthCheckConfig' in entry:
                key = entry['HealthCheckConfig']
                if key['IPAddress'] == master_ip:
                    print entry['Id']
                    return entry['Id']


def delete_dns_record(zone_id, domain_name, record_type, master_ip):
    response = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': record_type,
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': master_ip
                            }
                        ]
                    }
                }
            ]
        }
    )
    print("Response code %s " % response['ResponseMetadata']['HTTPStatusCode'])


if __name__ == '__main__':
    domain_name = 'test.com.'                          # CHANGEME !!!!
    record_master_ident = 'test-primary'            # CHANGEME !!!!
    record_slave_ident = 'test-secondary'           # CHANGEME !!!!
    master_ip = '1.1.1.1'                         # CHANGEME !!!!
    slave_ip = '1.1.1.2'                          # CHANGEME !!!!
    caller_ref = 'test-lbl-01'                          # CHANGEME !!!!

    failover_master_role = 'PRIMARY'
    failover_slave_role = 'SECONDARY'

    record_type = 'A'                                   # 'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'

    ttl = 10
    check_port = 80
    check_type = 'HTTP'                 # 'HTTP'|'HTTPS'|'HTTP_STR_MATCH'|'HTTPS_STR_MATCH'|'TCP'|'CALCULATED'|'CLOUDWATCH_METRIC'
    check_path = '/'
    check_interval = 10
    check_failed_threshold = 2

    zone_id=get_zone_id(domain_name)
    if zone_id is not None:
        create_healthcheck(caller_ref, master_ip, check_port, check_type, check_path, check_interval, check_failed_threshold)
        healthcheck_id = get_healthchecks_id_by_ip(master_ip)
        delete_dns_record(zone_id, domain_name, record_type, master_ip)
        create_master_record(zone_id, domain_name, record_type, record_master_ident, master_ip, failover_master_role, ttl, healthcheck_id)
        create_slave_record(zone_id, domain_name, record_type, record_slave_ident, slave_ip, failover_slave_role, ttl)
        list_records_by_id(zone_id)
        list_failovers(zone_id)
    else:
        print 'Zone Not exists'
