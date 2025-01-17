# File: netskope_view.py
#
# Copyright 2018-2025 Netskope, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
from datetime import datetime


def get_ctx_result(provides, result):
    """Parse the data.

    :param result: result
    :param provides: action name
    :return: response data
    """
    ctx_result = {}
    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()
    ctx_result["param"] = param
    if summary:
        ctx_result["summary"] = summary
    ctx_result["action"] = provides
    if not data:
        ctx_result["data"] = {}
        return ctx_result
    ctx_result["data"] = _parse_data(data[0])
    return ctx_result


def _parse_data(data):
    """Parse the data.

    :param data: response data
    :return: response data
    """
    for pages in data.get("page", []):
        try:
            if pages.get("_insertion_epoch_timestamp"):
                pages["_insertion_epoch_timestamp"] = ("{}Z").format(datetime.fromtimestamp(pages["_insertion_epoch_timestamp"]).isoformat())
        except ValueError:
            pass

    for app in data.get("application", []):
        try:
            if app.get("_insertion_epoch_timestamp"):
                app["_insertion_epoch_timestamp"] = ("{}Z").format(datetime.fromtimestamp(app["_insertion_epoch_timestamp"]).isoformat())
        except ValueError:
            pass

    return data


def display_view(provides, all_app_runs, context):
    """Display view.

    :param provides: action name
    :param context: context
    :param all_app_runs: all app runs
    :return: html page
    """
    context["results"] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:
            ctx_result = get_ctx_result(provides, result)
            if not ctx_result:
                continue
            results.append(ctx_result)

    return_page = "netskope_run_query.html"
    return return_page
