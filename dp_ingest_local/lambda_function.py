from .ingest import ingest_comment, ingest_docket, ingest_document

def lambda_handler(event, context):
    docket = """
    {
        "data": {
            "attributes": {
                "agencyId": "DOS",
                "category": "Public Notices - None Rule Related",
                "displayProperties": [
                    {
                        "label": "Effective Date",
                        "name": "effectiveDate",
                        "tooltip": "An agency- specified date associated with a docket (regulatory action)."
                    }
                ],
                "dkAbstract": "SUMMARY: The Department of State is amending the International Traffic in Arms Regulations (ITAR) to better organize the purposes and definitions of the regulations. This rule consolidates and co-locates authorities, general guidance, and definitions.",
                "docketType": "Rulemaking",
                "effectiveDate": "2022-09-06T04:00:00Z",
                "field1": null,
                "field2": null,
                "generic": null,
                "keywords": [
                    "DOSAR",
                    "60 Day Information Collection",
                    "Counsular Affairs",
                    "African Affairs",
                    "30 Day Information Collection",
                    "Aliens",
                    "Arms Export",
                    "Counterterrorism",
                    "Arms Control"
                ],
                "legacyId": null,
                "modifyDate": "2023-01-05T11:19:18Z",
                "objectId": "0b00006484f6e7f3",
                "organization": null,
                "petitionNbr": null,
                "program": null,
                "rin": "1400-AE27",
                "shortTitle": null,
                "subType": "ITAR",
                "subType2": null,
                "title": "International Traffic in Arms Regulations: Consolidation and Restructuring of Purposes and Definitions"
                },
            "id": "DOS-2022-0004",
            "links": {
                "self": "https://api.regulations.gov/v4/dockets/DOS-2022-0004"
            },
            "type": "dockets"
        }
    }
    """

    document = """
    {
        "data": {
            "attributes": {
                "additionalRins": null,
                "address1": null,
                "address2": null,
                "agencyId": "DOS",
                "allowLateComments": false,
                "authorDate": null,
                "authors": null,
                "category": null,
                "cfrPart": "22 CFR Parts 120, 121, 122, 123, 124, 125, 126",
                "city": null,
                "comment": null,
                "commentEndDate": "2022-05-10T03:59:59Z",
                "commentStartDate": "2022-03-23T04:00:00Z",
                "country": null,
                "displayProperties": [
                    {
                        "label": "Page Count",
                        "name": "pageCount",
                        "tooltip": "Number of pages In the content file"
                    }
                ],
                "docAbstract": null,
                "docketId": "DOS-2022-0004",
                "documentType": "Rule",
                "effectiveDate": null,
                "email": null,
                "exhibitLocation": null,
                "exhibitType": null,
                "fax": null,
                "field1": null,
                "field2": null,
                "fileFormats": [
                    {
                        "fileUrl": "https://downloads.regulations.gov/DOS-2022-0004-0001/content.pdf",
                        "format": "pdf",
                        "size": 756575
                    },
                    {
                        "fileUrl": "https://downloads.regulations.gov/DOS-2022-0004-0001/content.htm",
                        "format": "htm",
                        "size": 154561
                    }
                ],
                "firstName": null,
                "frDocNum": "2022-05629",
                "frVolNum": null,
                "govAgency": null,
                "govAgencyType": null,
                "implementationDate": null,
                "lastName": null,
                "legacyId": null,
                "media": null,
                "modifyDate": "2022-05-10T01:01:14Z",
                "objectId": "0900006484fdb1f2",
                "ombApproval": null,
                "openForComment": false,
                "organization": null,
                "originalDocumentId": "DOS_FRDOC_0001-5785",
                "pageCount": 31,
                "paperLength": 0,
                "paperWidth": 0,
                "phone": null,
                "postedDate": "2022-03-23T04:00:00Z",
                "postmarkDate": null,
                "reasonWithdrawn": null,
                "receiveDate": "2022-03-23T04:00:00Z",
                "regWriterInstruction": null,
                "restrictReason": null,
                "restrictReasonType": null,
                "sourceCitation": null,
                "startEndPage": "16396 - 16426",
                "stateProvinceRegion": null,
                "subject": "Arms and Munitions, Classified Information, Exports, Reporting and Recordkeeping, Technical Assistance, Crime, Penalties, Seizures and Forfeitures, Administrative Practice and Procedure, Brok",
                "submitterRep": null,
                "submitterRepAddress": null,
                "submitterRepCityState": null,
                "subtype": null,
                "title": "International Traffic in Arms: Consolidation and Restructuring of Purposes and Definitions",
                "topics": [
                    "Arms and Munitions",
                    "Classified Information",
                    "Exports",
                    "Reporting and Recordkeeping Requirements",
                    "Technical Assistance",
                    "Crime",
                    "Penalties",
                    "Seizures and Forfeitures",
                    "Administrative Practices and Procedures",
                    "Brokers",
                    "Campaign Funds",
                    "Confidential Business Information"
                ],
                "trackingNbr": null,
                "withdrawn": false,
                "zip": null
                },
                "id": "DOS-2022-0004-0001",
                "links": {
                    "self": "https://api.regulations.gov/v4/documents/DOS-2022-0004-0001"
                },
            "relationships": {
                "attachments": {
                    "links": {
                        "related": "https://api.regulations.gov/v4/documents/DOS-2022-0004-0001/attachments",
                        "self": "https://api.regulations.gov/v4/documents/DOS-2022-0004-0001/relationships/attachments"
                    }
                }
            },
            "type": "documents"
        }
    }
    """

    comment = """
{
"data": {
"id": "DOS-2022-0004-0003",
"type": "comments",
"links": {
"self": "https://api.regulations.gov/v4/comments/DOS-2022-0004-0003"
},
"attributes": {
"commentOn": "0900006484fdb1f2",
"commentOnDocumentId": "DOS-2022-0004-0001",
"duplicateComments": 0,
"address1": null,
"address2": null,
"agencyId": "DOS",
"city": null,
"category": null,
"comment": "See attached file(s)",
"country": null,
"displayProperties": [
{
"name": "pageCount",
"label": "Page Count",
"tooltip": "Number of pages In the content file"
}
],
"docAbstract": null,
"docketId": "DOS-2022-0004",
"documentType": "Public Submission",
"email": null,
"fax": null,
"field1": null,
"field2": null,
"fileFormats": null,
"firstName": null,
"govAgency": null,
"govAgencyType": null,
"objectId": "0900006485063c49",
"lastName": null,
"legacyId": null,
"modifyDate": "2022-05-12T15:52:38Z",
"organization": "Raytheon Technologies Corporation",
"originalDocumentId": null,
"pageCount": 1,
"phone": null,
"postedDate": "2022-05-10T04:00:00Z",
"postmarkDate": null,
"reasonWithdrawn": null,
"receiveDate": "2022-05-09T04:00:00Z",
"restrictReason": null,
"restrictReasonType": null,
"stateProvinceRegion": null,
"submitterRep": null,
"submitterRepAddress": null,
"submitterRepCityState": null,
"subtype": null,
"title": "Comment on DOS-2022-0004-0001",
"trackingNbr": "l2z-02tq-bsbu",
"withdrawn": false,
"zip": null,
"openForComment": false
},
"relationships": {
"attachments": {
"data": [
{
"id": "0900006485063c4a",
"type": "attachments"
}
],
"links": {
"self": "https://api.regulations.gov/v4/comments/DOS-2022-0004-0003/relationships/attachments",
"related": "https://api.regulations.gov/v4/comments/DOS-2022-0004-0003/attachments"
}
}
}
},
"included": [
{
"id": "0900006485063c4a",
"type": "attachments",
"links": {
"self": "https://api.regulations.gov/v4/attachments/0900006485063c4a"
},
"attributes": {
"agencyNote": null,
"authors": null,
"docAbstract": null,
"docOrder": 1,
"fileFormats": [
{
"fileUrl": "https://downloads.regulations.gov/DOS-2022-0004-0003/attachment_1.pdf",
"format": "pdf",
"size": 235577
}
],
"modifyDate": "2022-05-09T13:41:01Z",
"publication": null,
"restrictReason": null,
"restrictReasonType": null,
"title": "Raytheon Technologies Corp. Comments re DOS-2022-0004"
}
}
]
}
    """

    ingest_docket(docket)
    ingest_document(document)
    ingest_comment(comment)
