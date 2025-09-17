{% set data_description = lyr_metadata.data_description %}
{% set temporal_scope = lyr_metadata.temporal_scope %}
{% set geographic_scope = lyr_metadata.geographic_scope %}
{% set taxonomic_scope = lyr_metadata.taxonomic_scope %}
{% set methodology = lyr_metadata.methodology %}
{% set citation = lyr_metadata.citation %}

#### Description

{{ data_description.dataset_description }}

**Tags:** _{{ data_description.keywords }}_

#### Temporal scope

{{ temporal_scope.temporal_description }}

**Aquisition period:** _{{ temporal_scope.temporal_scope }}_

#### Geographic scope

{{ geographic_scope.location_description }}

**Location:** _{{ geographic_scope.country }}, {{ geographic_scope.county_name }}, {{ geographic_scope.municipality_name }} ({{ geographic_scope.municipality_code }})_

#### Taxonomic scope

{{ taxonomic_scope.taxonomic_description }}

{% if taxonomic_scope.taxa %}
**Taxa:**
{% for word in taxonomic_scope.taxa.split(';') %}

- {{ word.strip() }}
  {% endfor %}
  {% endif %}

#### Methodology

{{ methodology.method_description|safe }}

{% if methodology.doc_url %}

- **Documentation webpage:** [{{ methodology.doc_string }}]({{ methodology.doc_url }})
  {% endif %}
  {% if methodology.aquisition_method %}
- **Acquisition method:** {{ methodology.aquisition_method }}
- **Unit:** {{ methodology.unit }}
- **Measuring scale:** {{ methodology.measuring_scale }}
- **Platform:** {{ methodology.platform }}
- **Sensor:** {{ methodology.sensor }}
- **Spatial resolution:** {{ methodology.spatial_resolution }}
- **Temporal resolution:** {{ methodology.temporal_resolution }}
  {% endif %}

#### Data description

- **Project ID:** {{data_description.project_id}}
- **Data type:** {{data_description.data_type}}
- **File type:** {{data_description.file_type}}
- **Dataset name:** {{data_description.dataset_name}}
- **Dataset alias:** {{data_description.dataset_alias}}
- **Ecosystem accounting category:** {{data_description.category_ecosystem_accounting}}
- **License:** {{data_description.license}}
- **Data language:** {{data_description.data_language}}
- **Metadata language:** {{data_description.metadata_language}}
- **Dataset owner:** {{data_description.dataset_owner}}
- **Dataset manager:** {{data_description.dataset_manager}}

#### Contacts

{% for contact in project.contacts %}
**{{ contact.firstName }} {{ contact.lastName }}**

- **Role:** {{ contact.contactType }}
- **Organisation:** {{ contact.organisationName }}
- **Email:** [{{ contact.email }}](mailto:{{ contact.email }})
- **Orcid:** [{{ contact.orcid }}]({{ contact.orcid }})

{% endfor %}

#### Citation

{% if citation.reference_string %}
[{{ citation.reference_string }}]({{ citation.reference_url }})
{% endif %}
