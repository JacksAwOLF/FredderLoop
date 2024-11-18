def _add_paragraph(
    text: str,
    curr_ind: int,
    heading_type: str,
    newline: bool = True,
) -> tuple[list, int]:
    requests = []
    new_text = text
    if newline:
        new_text = f"{text}\n"
    change_len = len(text) + 1
    requests.append(
        {
            "insertText": {"text": new_text, "location": {"index": curr_ind}},
        }
    )
    if heading_type:
        requests.append(
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": curr_ind,
                        "endIndex": curr_ind + change_len,
                    },
                    "fields": "namedStyleType",
                    "paragraphStyle": {"namedStyleType": heading_type},
                },
            },
        )
    return requests, curr_ind + change_len


def _add_table_answers(
    contents: dict,
    curr_ind: int,
    num_cols: int = 1,
    set_bg_color: bool = True,
) -> tuple[list, int]:
    requests = []
    for name, answers in contents.items():
        num_rows = -(len(answers) // -num_cols)  # ceiling

        # add name
        tmp, curr_ind = _add_paragraph(
            text=name,
            curr_ind=curr_ind,
            heading_type="HEADING_2",
            newline=True,
        )
        requests.extend(tmp)

        # create table of num_cols number of columns and as many rows as necessary
        og_table_index = curr_ind  # for deleting random newline later
        requests.append(
            {
                "insertTable": {
                    "columns": num_cols,
                    # "endOfSegmentLocation": {},
                    "location": {
                        "index": curr_ind,
                    },
                    "rows": num_rows,
                }
            }
        )

        # temp increase curr_ind due to random newline from table insert
        curr_ind += 1

        # transform answers into table-like format first
        transformed_ans = []
        tmp = []
        for i_ans, ans in enumerate(answers):
            tmp.append(ans)
            if (i_ans + 1) % num_cols == 0:  #
                transformed_ans.append(tmp)
                tmp = []
        if len(tmp) > 0:
            while len(tmp) < num_cols:
                tmp.append("")
            transformed_ans.append(tmp)

        # add answers to table
        for row in transformed_ans:
            curr_ind += 1  # add index per row
            for ans in row:
                curr_ind += 2
                # weird google math? 1 for cell and one for newline maybe?
                tmp, curr_ind = _add_paragraph(
                    text=ans,
                    curr_ind=curr_ind,
                    heading_type="NORMAL_TEXT",
                    newline=False,
                )
                requests.extend(tmp)

        requests.append(
            {
                "deleteContentRange": {
                    "range": {
                        # don't know why it needs to be minus 1, maybe am deleting the added newline rather than the random newline?
                        "startIndex": og_table_index - 1,
                        "endIndex": og_table_index,
                    }
                }
            }
        )

        if set_bg_color:
            requests.append(
                {
                    "updateTableCellStyle": {
                        "fields": "backgroundColor, borderBottom, borderLeft, borderRight, borderTop",
                        "tableCellStyle": {
                            "backgroundColor": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.9607843,
                                        "green": 0.9607843,
                                        "blue": 0.9607843,
                                    },
                                },
                            },
                            "borderBottom": {
                                "color": {
                                    "color": {
                                        "rgbColor": {
                                            "red": 0.7,
                                            "green": 0.7,
                                            "blue": 0.7,
                                        }
                                    }
                                },
                                "dashStyle": "SOLID",
                                "width": {
                                    "magnitude": 1,
                                    "unit": "PT",
                                },
                            },
                            "borderLeft": {
                                "color": {
                                    "color": {
                                        "rgbColor": {
                                            "red": 0.7,
                                            "green": 0.7,
                                            "blue": 0.7,
                                        }
                                    }
                                },
                                "dashStyle": "SOLID",
                                "width": {
                                    "magnitude": 1,
                                    "unit": "PT",
                                },
                            },
                            "borderRight": {
                                "color": {
                                    "color": {
                                        "rgbColor": {
                                            "red": 0.7,
                                            "green": 0.7,
                                            "blue": 0.7,
                                        }
                                    }
                                },
                                "dashStyle": "SOLID",
                                "width": {
                                    "magnitude": 1,
                                    "unit": "PT",
                                },
                            },
                            "borderTop": {
                                "color": {
                                    "color": {
                                        "rgbColor": {
                                            "red": 0.7,
                                            "green": 0.7,
                                            "blue": 0.7,
                                        }
                                    }
                                },
                                "dashStyle": "SOLID",
                                "width": {
                                    "magnitude": 1,
                                    "unit": "PT",
                                },
                            },
                        },
                        "tableRange": {
                            "columnSpan": num_cols,
                            "rowSpan": num_rows,
                            "tableCellLocation": {
                                "columnIndex": 0,
                                "rowIndex": 0,
                                "tableStartLocation": {
                                    "index": og_table_index,
                                },
                            },
                        },
                    },
                },
            )

        # curr_ind += 1 # don't add another, since added temp earlier
        tmp, curr_ind = _add_paragraph(
            text="", curr_ind=curr_ind, heading_type=""
        )  # add newline
        requests.extend(tmp)

    return requests, curr_ind


def add_title(title: str, curr_ind: int) -> tuple[list, int]:
    return _add_paragraph(text=title, curr_ind=curr_ind, heading_type="TITLE")


def add_horizontal_rule(curr_ind: int) -> tuple[list, int]:
    requests = []
    ind_change = 0
    requests.append(
        {
            "insertTable": {
                "columns": 1,
                "location": {
                    "index": curr_ind,
                },
                "rows": 1,
            },
        },
    )
    ind_change += 5
    requests.append(
        {
            "updateTableCellStyle": {
                "fields": "borderBottom, borderLeft, borderRight, borderTop, paddingBottom, paddingLeft, paddingRight, paddingTop",
                "tableCellStyle": {
                    "borderBottom": {
                        "color": {
                            "color": {
                                "rgbColor": {
                                    "red": 0.7,
                                    "green": 0.7,
                                    "blue": 0.7,
                                }
                            }
                        },
                        "dashStyle": "SOLID",
                        "width": {
                            "magnitude": 0,
                            "unit": "PT",
                        },
                    },
                    "borderLeft": {
                        "color": {
                            "color": {
                                "rgbColor": {
                                    "red": 0.7,
                                    "green": 0.7,
                                    "blue": 0.7,
                                }
                            }
                        },
                        "dashStyle": "SOLID",
                        "width": {
                            "magnitude": 0,
                            "unit": "PT",
                        },
                    },
                    "borderRight": {
                        "color": {
                            "color": {
                                "rgbColor": {
                                    "red": 0.7,
                                    "green": 0.7,
                                    "blue": 0.7,
                                }
                            }
                        },
                        "dashStyle": "SOLID",
                        "width": {
                            "magnitude": 0,
                            "unit": "PT",
                        },
                    },
                    "borderTop": {
                        "color": {
                            "color": {
                                "rgbColor": {
                                    "red": 0.6,
                                    "green": 0.6,
                                    "blue": 0.6,
                                }
                            }
                        },
                        "dashStyle": "SOLID",
                        "width": {
                            "magnitude": 1.5,
                            "unit": "PT",
                        },
                    },
                    "paddingBottom": {
                        "magnitude": 0,
                        "unit": "PT",
                    },
                    "paddingLeft": {
                        "magnitude": 0,
                        "unit": "PT",
                    },
                    "paddingRight": {
                        "magnitude": 0,
                        "unit": "PT",
                    },
                    "paddingTop": {
                        "magnitude": 0,
                        "unit": "PT",
                    },
                },
                "tableRange": {
                    "columnSpan": 1,
                    "rowSpan": 1,
                    "tableCellLocation": {
                        "columnIndex": 0,
                        "rowIndex": 0,
                        "tableStartLocation": {
                            "index": curr_ind + 1,
                        },
                    },
                },
            },
        },
    )
    requests.append(
        {
            "updateTextStyle": {
                "fields": "fontSize",
                "range": {
                    "endIndex": curr_ind + 3,
                    "startIndex": curr_ind + 2,
                },
                "textStyle": {
                    "fontSize": {
                        "magnitude": 3,
                        "unit": "PT",
                    },
                },
            },
        },
    )

    requests.append(
        {
            "deleteContentRange": {
                "range": {
                    # don't know why it needs to be minus 1, maybe am deleting the added newline rather than the random newline?
                    "startIndex": curr_ind - 1,
                    "endIndex": curr_ind,
                }
            }
        }
    )
    return requests, curr_ind + ind_change


def add_response(response: dict, curr_index: int) -> tuple[list, int]:
    requests = []
    # add question
    question = list(response.keys())[0]
    tmp, curr_index = _add_paragraph(
        text=question, curr_ind=curr_index, heading_type="HEADING_1"
    )
    requests.extend(tmp)

    # add name + answers
    tmp, curr_index = _add_table_answers(
        contents=response[question], curr_ind=curr_index, num_cols=1
    )
    requests.extend(tmp)
    return requests, curr_index


def add_photos(response: dict, curr_ind: int) -> tuple[list, int]:
    requests = []

    # add question
    question = list(response.keys())[0]
    tmp, curr_ind = _add_paragraph(
        text=question, curr_ind=curr_ind, heading_type="HEADING_1"
    )
    requests.extend(tmp)

    # add name + photos
    num_cols = 2
    for name, photos in response[question].items():
        num_rows = -(len(photos) // -num_cols)  # ceiling
        # add name
        tmp, curr_ind = _add_paragraph(
            text=name,
            curr_ind=curr_ind,
            heading_type="HEADING_2",
            newline=True,
        )
        requests.extend(tmp)

        # create 2 x Y table
        og_table_index = curr_ind  # for deleting random newline later
        requests.append(
            {
                "insertTable": {
                    "columns": num_cols,
                    "location": {
                        "index": curr_ind,
                    },
                    "rows": num_rows,
                },
            },
        )

        # temp increase curr_ind due to random newline from table insert
        curr_ind += 1

        # transform photo ids into table-like format first
        transformed_ids = []
        tmp = []
        for i_id, id in enumerate(photos):
            tmp.append(id)
            if (i_id + 1) % num_cols == 0:
                transformed_ids.append(tmp)
                tmp = []
        if len(tmp) > 0:
            while len(tmp) < num_cols:
                tmp.append("")
            transformed_ids.append(tmp)

        for row in transformed_ids:
            curr_ind += 1  # add index per row
            for photo_id in row:
                curr_ind += 2
                if photo_id == "":
                    # curr_ind += 1
                    continue
                # get image
                requests.append(
                    {
                        "insertInlineImage": {
                            "location": {
                                "index": curr_ind,
                            },
                            # "uri": f"https://drive.google.com/uc?export=view&id={photo_id}",
                            # use below for auto convert image type
                            "uri": f"https://drive.google.com/thumbnail?id="
                            + photo_id
                            + "&sz=w1000",
                        },
                    },
                )
                curr_ind += 1  # to account for image

        requests.append(
            {
                "deleteContentRange": {
                    "range": {
                        "startIndex": og_table_index - 1,
                        "endIndex": og_table_index,
                    },
                },
            },
        )

        requests.append(
            {
                "updateTableCellStyle": {
                    "fields": "borderBottom, borderLeft, borderRight, borderTop",
                    "tableCellStyle": {
                        "borderBottom": {
                            "color": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.7,
                                        "green": 0.7,
                                        "blue": 0.7,
                                    }
                                }
                            },
                            "dashStyle": "SOLID",
                            "width": {
                                "magnitude": 0,
                                "unit": "PT",
                            },
                        },
                        "borderLeft": {
                            "color": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.7,
                                        "green": 0.7,
                                        "blue": 0.7,
                                    }
                                }
                            },
                            "dashStyle": "SOLID",
                            "width": {
                                "magnitude": 0,
                                "unit": "PT",
                            },
                        },
                        "borderRight": {
                            "color": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.7,
                                        "green": 0.7,
                                        "blue": 0.7,
                                    }
                                }
                            },
                            "dashStyle": "SOLID",
                            "width": {
                                "magnitude": 0,
                                "unit": "PT",
                            },
                        },
                        "borderTop": {
                            "color": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.6,
                                        "green": 0.6,
                                        "blue": 0.6,
                                    }
                                }
                            },
                            "dashStyle": "SOLID",
                            "width": {
                                "magnitude": 0,
                                "unit": "PT",
                            },
                        },
                    },
                    "tableRange": {
                        "columnSpan": num_cols,
                        "rowSpan": num_rows,
                        "tableCellLocation": {
                            "columnIndex": 0,
                            "rowIndex": 0,
                            "tableStartLocation": {
                                "index": og_table_index,
                            },
                        },
                    },
                },
            },
        )

        curr_ind += 1

        tmp, curr_ind = _add_paragraph(
            text="", curr_ind=curr_ind, heading_type=""
        )  # add newline
        requests.extend(tmp)
    return requests, curr_ind


def update_font(curr_ind: int) -> tuple[list, int]:
    requests = []
    requests.append(
        {
            "updateTextStyle": {
                "fields": "weightedFontFamily",
                "range": {
                    "endIndex": curr_ind - 1,
                    "startIndex": 1,
                },
                "textStyle": {
                    "weightedFontFamily": {
                        "fontFamily": "Comic Neue",
                        "weight": 700, # 300 light, 400 regular, 700 bold
                    }
                },
            }
        }
    )
    return requests, curr_ind