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
    SELECT addr_id, province, country_typ_cd, postal_cd, addr_line_1, addr_line_2, addr_line_3,
           city, address_format_type, address_desc, address_desc_short, delivery_instructions,
           unit_no, unit_type, civic_no, civic_no_suffix, street_name, street_type,
           street_direction, lock_box_no, installation_type, installation_name,
           installation_qualifier, route_service_type, route_service_no, province_state_name
      FROM address;


DROP PUBLIC SYNONYM ADDRESS_VW;

CREATE PUBLIC SYNONYM ADDRESS_VW FOR NAMEX.ADDRESS_VW;
