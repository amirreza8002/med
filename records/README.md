## models:
### condition
#### user (many to one, autofill, non editable)
#### name
#### severity (blank=True, null=True)
#### medicine (many to many, blank=True, null=True)


### medicine
#### name
#### descriptions (admin access only)


### description 
#### many to one with condition
#### inline form to condition (needs more work)