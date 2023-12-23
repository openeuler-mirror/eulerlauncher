# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: instances.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import flavors_pb2 as flavors__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0finstances.proto\x12\tinstances\x1a\rflavors.proto\"~\n\x08Instance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x10\n\x08vm_state\x18\x03 \x01(\t\x12\x12\n\nip_address\x18\x04 \x01(\t\x12$\n\x06\x66lavor\x18\x05 \x01(\x0b\x32\x0f.flavors.FlavorH\x00\x88\x01\x01\x42\t\n\x07_flavor\"\x16\n\x14ListInstancesRequest\"?\n\x15ListInstancesResponse\x12&\n\tinstances\x18\x01 \x03(\x0b\x32\x13.instances.Instance\"\x92\x01\n\x15\x43reateInstanceRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x0c\n\x04\x61rch\x18\x03 \x01(\t\x12\x15\n\rinstance_path\x18\x04 \x01(\t\x12\x16\n\x0eroot_disk_path\x18\x05 \x01(\t\x12\x1f\n\x06\x66lavor\x18\x06 \x01(\x0b\x32\x0f.flavors.Flavor\"k\n\x16\x43reateInstanceResponse\x12\x0b\n\x03ret\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12*\n\x08instance\x18\x03 \x01(\x0b\x32\x13.instances.InstanceH\x00\x88\x01\x01\x42\x0b\n\t_instance\"%\n\x15\x44\x65leteInstanceRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"2\n\x16\x44\x65leteInstanceResponse\x12\x0b\n\x03ret\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\"$\n\x14StartInstanceRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"#\n\x13StopInstanceRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"H\n\x13TakeSnapshotRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08snapshot\x18\x02 \x01(\t\x12\x11\n\tdest_path\x18\x03 \x01(\t\"#\n\x14TakeSnapshotResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t\"\\\n\x1d\x45xportDevelopmentImageRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x11\n\tdest_path\x18\x03 \x01(\t\x12\x0b\n\x03pwd\x18\x04 \x01(\t\"-\n\x1e\x45xportDevelopmentImageResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t\"H\n\x11\x41ttachDiskRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tdisk_path\x18\x02 \x01(\t\x12\x12\n\ndrive_type\x18\x03 \x01(\t\"4\n\x11\x44\x65tachDiskRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tdisk_path\x18\x02 \x01(\t\"#\n\x10InstanceResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xb5\x07\n\x13InstanceGrpcService\x12U\n\x0elist_instances\x12\x1f.instances.ListInstancesRequest\x1a .instances.ListInstancesResponse\"\x00\x12X\n\x0f\x63reate_instance\x12 .instances.CreateInstanceRequest\x1a!.instances.CreateInstanceResponse\"\x00\x12X\n\x0f\x64\x65lete_instance\x12 .instances.DeleteInstanceRequest\x1a!.instances.DeleteInstanceResponse\"\x00\x12P\n\x0estart_instance\x12\x1f.instances.StartInstanceRequest\x1a\x1b.instances.InstanceResponse\"\x00\x12O\n\x0estop_instsance\x12\x1e.instances.StopInstanceRequest\x1a\x1b.instances.InstanceResponse\"\x00\x12G\n\nAttachDisk\x12\x1c.instances.AttachDiskRequest\x1a\x1b.instances.InstanceResponse\x12G\n\nDetachDisk\x12\x1c.instances.DetachDiskRequest\x1a\x1b.instances.InstanceResponse\x12J\n\x0b\x61ttach_disk\x12\x1c.instances.AttachDiskRequest\x1a\x1b.instances.InstanceResponse\"\x00\x12K\n\x0c\x64\x65ttach_disk\x12\x1c.instances.DetachDiskRequest\x1a\x1b.instances.InstanceResponse\"\x00\x12R\n\rtake_snapshot\x12\x1e.instances.TakeSnapshotRequest\x1a\x1f.instances.TakeSnapshotResponse\"\x00\x12q\n\x18\x65xport_development_image\x12(.instances.ExportDevelopmentImageRequest\x1a).instances.ExportDevelopmentImageResponse\"\x00\x42\x03\x80\x01\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'instances_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\200\001\001'
  _globals['_INSTANCE']._serialized_start=45
  _globals['_INSTANCE']._serialized_end=171
  _globals['_LISTINSTANCESREQUEST']._serialized_start=173
  _globals['_LISTINSTANCESREQUEST']._serialized_end=195
  _globals['_LISTINSTANCESRESPONSE']._serialized_start=197
  _globals['_LISTINSTANCESRESPONSE']._serialized_end=260
  _globals['_CREATEINSTANCEREQUEST']._serialized_start=263
  _globals['_CREATEINSTANCEREQUEST']._serialized_end=409
  _globals['_CREATEINSTANCERESPONSE']._serialized_start=411
  _globals['_CREATEINSTANCERESPONSE']._serialized_end=518
  _globals['_DELETEINSTANCEREQUEST']._serialized_start=520
  _globals['_DELETEINSTANCEREQUEST']._serialized_end=557
  _globals['_DELETEINSTANCERESPONSE']._serialized_start=559
  _globals['_DELETEINSTANCERESPONSE']._serialized_end=609
  _globals['_STARTINSTANCEREQUEST']._serialized_start=611
  _globals['_STARTINSTANCEREQUEST']._serialized_end=647
  _globals['_STOPINSTANCEREQUEST']._serialized_start=649
  _globals['_STOPINSTANCEREQUEST']._serialized_end=684
  _globals['_TAKESNAPSHOTREQUEST']._serialized_start=686
  _globals['_TAKESNAPSHOTREQUEST']._serialized_end=758
  _globals['_TAKESNAPSHOTRESPONSE']._serialized_start=760
  _globals['_TAKESNAPSHOTRESPONSE']._serialized_end=795
  _globals['_EXPORTDEVELOPMENTIMAGEREQUEST']._serialized_start=797
  _globals['_EXPORTDEVELOPMENTIMAGEREQUEST']._serialized_end=889
  _globals['_EXPORTDEVELOPMENTIMAGERESPONSE']._serialized_start=891
  _globals['_EXPORTDEVELOPMENTIMAGERESPONSE']._serialized_end=936
  _globals['_ATTACHDISKREQUEST']._serialized_start=938
  _globals['_ATTACHDISKREQUEST']._serialized_end=1010
  _globals['_DETACHDISKREQUEST']._serialized_start=1012
  _globals['_DETACHDISKREQUEST']._serialized_end=1064
  _globals['_INSTANCERESPONSE']._serialized_start=1066
  _globals['_INSTANCERESPONSE']._serialized_end=1101
  _globals['_INSTANCEGRPCSERVICE']._serialized_start=1104
  _globals['_INSTANCEGRPCSERVICE']._serialized_end=2053
# @@protoc_insertion_point(module_scope)
