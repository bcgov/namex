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
"""Manages solr doc updates made to the Search Core (tracks updates made via the api)."""
from __future__ import annotations

from datetime import UTC, datetime
from enum import auto
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, event, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from namex_solr_api.common.base_enum import BaseEnum

from .base import Base
from .db import db

if TYPE_CHECKING:
    from namex_solr_api.models.solr_doc import SolrDoc


class SolrDocEvent(Base):
    """Used to hold event information for a solr doc."""
    
    class Status(BaseEnum):
        """Enum of the solr doc event statuses."""

        COMPLETE = auto()
        ERROR = auto()
        PENDING = auto()
    
    class Type(BaseEnum):
        """Enum of the solr doc event types."""
        
        RESYNC = auto()  # event for re-applying an entity update to solr
        UPDATE = auto()  # event for applying an entity update to solr

    __tablename__ = "solr_doc_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    event_last_update: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    event_status: Mapped[Status] = mapped_column(default=Status.PENDING.value, index=True)
    event_type: Mapped[Type]

    solr_doc_id: Mapped[int] = mapped_column(ForeignKey('solr_docs.id'), index=True)
    solr_doc: Mapped[SolrDoc] = relationship(back_populates='events')

    @classmethod
    def get_events_by_status(
        cls,
        statuses: list[Status],
        event_types: list[Type] | None = None,
        start_date: datetime | None = None,
        limit: int | None = None,
    ) -> list[SolrDocEvent]:
        """Update the status of the given events."""
        query = cls.query.filter(cls.event_status.in_(statuses))
        if event_types:
            query = query.filter(cls.event_type.in_(event_types))
        if start_date:
            query = query.filter(cls.event_date > start_date)

        query = query.order_by(cls.event_date)
        if limit:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def update_events_status(cls, status: Status, events: list[SolrDocEvent]):
        """Update the status of the given events."""
        for doc_event in events:
            if doc_event is None:
                continue
            doc_event.event_status = status
            db.session.add(doc_event)
        db.session.commit()


@event.listens_for(SolrDocEvent, "before_update")
def receive_before_change(mapper, connection, target: SolrDocEvent):
    """Set the last updated value."""
    target.event_last_update = datetime.now(UTC)
