-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.ADDRESS_VW;

CREATE OR REPLACE FORCE VIEW namex.address_vw (addr_id,
                                               province,
                                               country_typ_cd,
                                               postal_cd,
                                               addr_line_1,
                                               addr_line_2,
                                               addr_line_3,
                                               city,
                                               address_format_type,
                                               address_desc,
                                               address_desc_short,
                                               delivery_instructions,
                                               unit_no,
                                               unit_type,
                                               civic_no,
                                               civic_no_suffix,
                                               street_name,
                                               street_type,
                                               street_direction,
                                               lock_box_no,
                                               installation_type,
                                               installation_name,
                                               installation_qualifier,
                                               route_service_type,
                                               route_service_no,
                                               province_state_name
                                              )
AS
    SELECT "ADDR_ID", "PROVINCE", "COUNTRY_TYP_CD", "POSTAL_CD", "ADDR_LINE_1", "ADDR_LINE_2",
           "ADDR_LINE_3", "CITY", "ADDRESS_FORMAT_TYPE", "ADDRESS_DESC", "ADDRESS_DESC_SHORT",
           "DELIVERY_INSTRUCTIONS", "UNIT_NO", "UNIT_TYPE", "CIVIC_NO", "CIVIC_NO_SUFFIX",
           "STREET_NAME", "STREET_TYPE", "STREET_DIRECTION", "LOCK_BOX_NO", "INSTALLATION_TYPE",
           "INSTALLATION_NAME", "INSTALLATION_QUALIFIER", "ROUTE_SERVICE_TYPE", "ROUTE_SERVICE_NO",
           "PROVINCE_STATE_NAME"
      FROM address;


DROP PUBLIC SYNONYM ADDRESS_VW;

CREATE PUBLIC SYNONYM ADDRESS_VW FOR NAMEX.ADDRESS_VW;
