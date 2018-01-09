import sys
import boto3
import pprint
import time

class EC2:
    def __init__(self, query_filter):
        self.ec2 = boto3.resource('ec2')
        self.client = boto3.client('ec2')
        self.instances = self.get_instances(query_filter)

    def describe_instances(self):
        return self.client.describe_instances()

    def get_instances(self, query_filter):
        #http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.ServiceResource.instances
        return self.ec2.instances.filter(Filters=query_filter)

    def take_snapshot(self, ip, device):
        for instance in self.instances:
            #print instance.id, instance.instance_type, instance.state, instance.private_ip_address, instance.vpc_id
            if instance.private_ip_address == ip:
                volume_iterator = instance.volumes.all()
                for vol in volume_iterator:
                    #http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#volume
                    if vol.attachments[0]["Device"] == device:
                        print instance.id, instance.private_ip_address, vol.volume_id, vol.size
                        print "will take snapshot of this EBS volume"
                        start = time.clock()
                        response = ec2_inst.client.create_snapshot(DryRun=False, VolumeId=vol.volume_id, Description="braas test snapshot")
                        snap_id = response["SnapshotId"]
                        snapshot = ec2_inst.ec2.Snapshot(snap_id)
                        num_try = 0
                        while snapshot.state != 'completed':
                            print snapshot.progress, snapshot.id, snapshot.state, num_try
                            snapshot.load()
                            time.sleep(2)
                            num_try += 1
                        print "time taken to take snapshot", time.clock() - start, snapshot.state
                        return instance, snapshot.id

    def restore_snapshot(self, restore_inst, snap_id):
        #http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-restoring-volume.html
        #https://stackoverflow.com/questions/39302594/python-mount-ebs-volume-using-boto3/39326511
        self.client.create_volume(DryRun=True, SnapshotId=snap_id, AvailabilityZone = 'us-east-1')
        restore_inst.attach_volume(VolumeId

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    #query_filter = [{'Name': 'instance-state-name', 'Values': ['running']}, {}]
    query_filter = [{'Name': 'key-name', 'Values': ['braas-cc']}, {}]
    ec2_inst = EC2(query_filter)
    ec2_ip = sys.argv[1]
    instance, snap_id = ec2_inst.take_snapshot(ec2_ip, "/dev/sdb")


