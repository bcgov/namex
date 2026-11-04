# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""This manages a User record that can be used in an audit trail.

Actual user data is kept in the OIDC and IDP services, this data is
here as a convenience for audit and db reporting.
"""
from __future__ import annotations

from datetime import datetime  # noqa: TC003 ; sqlalchemy complains if its in a type block
from enum import auto
from typing import TYPE_CHECKING

from flask import current_app
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from namex_solr_api.common.base_enum import BaseEnum
from namex_solr_api.exceptions import BusinessException
from namex_solr_api.services import auth

from .base import Base
from .db import db

if TYPE_CHECKING:
    from namex_solr_api.models.search_history import SearchHistory
    from namex_solr_api.models.solr_doc import SolrDoc
    


class User(Base):
    """Used to hold the audit information for a User of this service."""

    class Role(BaseEnum):
        """Enum for the user roles."""
        system = auto()

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(1000), index=True)
    firstname: Mapped[str] = mapped_column(String(1000), nullable=True)
    lastname: Mapped[str] = mapped_column(String(1000), nullable=True)
    email: Mapped[str] = mapped_column(String(1000), nullable=True)
    login_source: Mapped[str] = mapped_column(String(200), nullable=True)
    sub: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    iss: Mapped[str] = mapped_column(String(1024))
    unique_user_key: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    # Relationships
    searches: Mapped[list[SearchHistory]] = relationship(back_populates="submitter")
    updated_docs: Mapped[list[SolrDoc]] = relationship(back_populates="submitter")

    @property
    def display_name(self):
        """Display name of user; do not show sensitive data like BCSC username.

        If there is actual name info, return that; otherwise username.
        """
        if self.firstname or self.lastname:
            return " ".join(filter(None, [self.firstname, self.lastname])).strip()

        # parse off idir\ or @idir
        if self.username:
            if self.username[:4] == "idir":
                return self.username[5:]
            if self.username[-4:] == "idir":
                return self.username[:-5]

            # do not show services card usernames
            if self.username[:4] == "bcsc":
                return None

        return self.username if self.username else None

    @classmethod
    def find_by_id(cls, submitter_id: int | None = None) -> User:
        """Return a User if they exist and match the provided submitter id."""
        return cls.query.filter_by(id=submitter_id).one_or_none()

    @classmethod
    def find_by_jwt_token(cls, token: dict) -> User:
        """Return a User if they exist and match the provided JWT."""
        if unique_jwt_field := current_app.config.get("JWT_OIDC_UNIQUE_USER_KEY"):
            return cls.query.filter_by(unique_user_key=token.get(unique_jwt_field, "unknown")).one_or_none()

    @classmethod
    def create_from_jwt_token(cls, token: dict):
        """Create a user record from the provided JWT token.

        Use the values found in the vaild JWT for the realm
        to populate the User audit data
        """
        if token:
            firstname = token.get(current_app.config.get("JWT_OIDC_FIRSTNAME"), None)
            lastname = token.get(current_app.config.get("JWT_OIDC_LASTNAME"), None)
            if token.get(current_app.config.get("JWT_OIDC_LOGIN_SOURCE"), None) == "BCEID":
                # bceid doesn't use the names from the token so have to get from auth
                auth_user = auth.get_user_info()
                firstname = auth_user["firstname"]
                lastname = auth_user["lastname"]

            user = User(
                username=token.get(current_app.config.get("JWT_OIDC_USERNAME"), None),
                firstname=firstname,
                lastname=lastname,
                iss=token["iss"],
                sub=token["sub"],
                login_source=token.get("loginSource", "unknown"),
                unique_user_key=token.get("idp_userid", "unknown"),
            )
            current_app.logger.debug("Creating user from JWT:%s; User:%s", token, user)
            db.session.add(user)
            db.session.commit()
            return user
        return None

    @classmethod
    def get_or_create_user_by_jwt(cls, jwt_oidc_token: dict):
        """Return a valid user for audit tracking purposes."""
        # GET existing or CREATE new user based on the JWT info
        try:
            user = User.find_by_jwt_token(jwt_oidc_token)
            current_app.logger.debug(f"finding user: {jwt_oidc_token}")
            if not user:
                current_app.logger.debug(f"didnt find user, attempting to create new user:{jwt_oidc_token}")
                user = User.create_from_jwt_token(jwt_oidc_token)
            elif jwt_oidc_token.get("loginSource") == "BCEID":  # BCEID doesn't use the jwt values for their name
                current_app.logger.debug("BCEID user, updating first and last names...")
                auth_user = auth.get_user_info()
                if user.firstname != auth_user["firstname"]:
                    user.firstname = auth_user["firstname"]
                if user.lastname != auth_user["lastname"]:
                    user.lastname = auth_user["lastname"]
                user.save()
                current_app.logger.debug("Updated user.")
            else:
                # update if there are any values that weren't saved previously or have changed since
                current_app.logger.debug("Checking for changes to jwt info...")
                user_keys = [
                    {"jwt_key": current_app.config.get("JWT_OIDC_USERNAME"), "table_key": "username"},
                    {"jwt_key": current_app.config.get("JWT_OIDC_FIRSTNAME"), "table_key": "firstname"},
                    {"jwt_key": current_app.config.get("JWT_OIDC_LASTNAME"), "table_key": "lastname"},
                    {"jwt_key": "sub", "table_key": "sub"},
                ]
                for keys in user_keys:
                    value = jwt_oidc_token.get(keys["jwt_key"], None)
                    if value and value != getattr(user, keys["table_key"]):
                        current_app.logger.debug(
                            f'found new user value, attempting to update user {keys["table_key"]}:{value}'
                        )
                        setattr(user, keys["table_key"], value)
                        user.save()
                        current_app.logger.debug(f"Updated user {value}.")

            return user
        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            raise BusinessException(message="Unable to get or create user.", error=err.with_traceback(None)) from err
