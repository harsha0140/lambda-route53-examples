# Python script, Lambda library &amp; Route 53 AWS service.

Here is python script which with helps of boto3 library can really fast configure DNS failover 
checks for domain with master and slave lbl hosts.

Route53 reference: [link](http://boto3.readthedocs.io/en/latest/reference/services/route53.html)  

# SETUP REQUIREMENTS 

To run this script you need:

0. `AWS KEY` and `Secret KEY`
1. Python (I used 2.7 version)
2. Imported boto3 library (I used python pip `pip install boto3`)

# How to use:

There are few functions to list current configuration on AWS Route53 side:

- list_all_records() : *list all record*
- list_hosted_zones() : *list hosted Zones*
- list_records_by_id(zone_id) : *Required Zone ID, lists records by Zone ID*
- list_health_cheks_by_zid(zone_id) : *Required Zone ID, lists health checks by Zone ID*
- list_failovers(zone_id) : *Required Zone ID, lists all failovers*
- get_zone_id(domain_name) : *Required domain name, return zone ID*
- create_healthcheck(caller_ref, master_ip, check_port, check_type, check_path, check_interval, check_failed_threshold) : *create health check for IP/domain*
- create_master_record(zid, domain, type, ident, ip, failover_role, ttl, healthcheck_id) : *create DNS failover record for master host*
- create_slave_record(zid, domain, type, ident, ip, failover_role, ttl) : *create DNS failover record for slave host*
- get_healthchecks_id_by_ip(master_ip) : *get healthcheck ID by master IP address*
- delete_dns_record(zone_id, domain_name, record_type, master_ip) : *delete DNS record* 

# List of variables
* AWS_KEY = '`AWS_KEY`'
* AWS_SEC_KEY = '`AWS_SEC_KEY`'
* domain_name = 'test.com.'                  `CHANGEME`
* record_master_ident = 'test-primary'       `CHANGEME`
* record_slave_ident = 'test-secondary'      `CHANGEME`
* master_ip = '1.1.1.1'                      `CHANGEME`
* slave_ip = '2.2.2.2'                       `CHANGEME`
* caller_ref = 'UniqueString'                `CHANGEME`
* failover_master_role = 'PRIMARY'
* failover_slave_role = 'SECONDARY'
* record_type = 'A'                          `'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'`
* ttl = 10
* check_port = 80
* check_type = 'HTTP'                        `'HTTP'|'HTTPS'|'HTTP_STR_MATCH'|'HTTPS_STR_MATCH'|'TCP'|'CALCULATED'|'CLOUDWATCH_METRIC'`
* check_path = '/'
* check_interval = 10
* check_failed_threshold = 2
