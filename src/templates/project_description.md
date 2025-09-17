#### Description

{{ project.projectDescription|safe }}

{% if project.projectKeywords %}
**Tags:** _{{ project.projectKeywords }}_
{% endif %}
{% if project.url %}
**Project webpage:** [{{ project.nameURL }}]({{ project.url }})
{% endif %}

#### Contacts

{% for contact in project.contacts %}
**{{ contact.firstName }} {{ contact.lastName }}**

- **Role:** {{ contact.contactType }}
- **Organisation:** {{ contact.organisationName }}
- **Email:** [{{ contact.email }}](mailto:{{ contact.email }})
- **Orcid:** [{{ contact.orcid }}]({{ contact.orcid }})

{% endfor %}

#### Project metadata

- **Project ID:** {{ project.projectID }}
- **Project title:** {{ project.projectTitle }}
- **Project short title:** {{ project.projectShortTitle }}
- **Project type:** {{ project.projectType }}
- **Project funding:** {{ project.projectFunding }}
- **Project period:** {{ project.projectPeriod }}
