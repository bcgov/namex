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
"""Solr formatting functions."""
import re


def parse_facets(facet_data: dict) -> dict:
    """Return formatted solr facet response data."""
    facet_info = facet_data.get("facets", {})
    facets = {}
    for category in facet_info:
        if category == "count":
            continue
        facets[category] = []
        for item in facet_info[category]["buckets"]:
            new_category = {"value": item["val"], "count": item["count"]}
            if parent_count := item.get("by_parent", None):
                new_category["parentCount"] = parent_count
            facets[category].append(new_category)

    return {"fields": facets}

def prep_query_str(query: str, dash: str | None = None, replace_and = True) -> str:
    r"""Return the query string prepped for solr call.

    Rules:
        - no doubles: &,+
        - escape beginning: +,-,/,!
        - escape everywhere: ",:,[,],*,~,<,>,?,\
        - remove: (,),^,{,},|,\
        - lowercase: all
        - (default) replace &,+ with ' and '
        - (optional) replace - with '', ' ', or ' - '
        - (optional) replace ' - ' with '-'
    """
    if not query:
        return ""

    rmv_doubles = r"([&+]){2,}"
    rmv_all = r"([()^{}|\\])"
    esc_begin = r"(^|\s)([+\-/!])"
    esc_all = r'([:~<>?\"\[\]])'
    special_and = r"([&+])"
    rmv_dash = r"(-)"
    pad_dash = r"(\S)(-)(\S)"
    tighten_dash = r"(\s+)(-)(\s+)"

    query = re.sub(rmv_doubles, r"\1", query.lower())
    query = re.sub(rmv_all, "", query)
    if replace_and:
        query = re.sub(special_and, r" and ", query)
    if dash:
        if dash == "replace":
            query = re.sub(rmv_dash, r" ", query)
        if dash == "remove":
            query = re.sub(rmv_dash, r"", query)
        if dash == "pad":
            query = re.sub(pad_dash, r"\1 \2 \3", query)
        if dash == "tighten":
            query = re.sub(tighten_dash, r"\2", query)
        if dash == "tighten-remove":
            query = re.sub(tighten_dash, r"", query)

    query = re.sub(esc_begin, r"\1\\\2", query)
    query = re.sub(esc_all, r"\\\1", query)
    return query.lower().replace("  ", " ").strip()
