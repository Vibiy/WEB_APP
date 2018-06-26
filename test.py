def update_graph_tab(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                     Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class], SQM=[SQM], Company=[Company],
                Business_Sector=[Business_Sector], Type_of_Deal=[Type_of_Deal],
                Type_of_Consultancy=[Type_of_Consultancy], Quarter=[Quarter],
                Include_in_Market_Share=[Include_in_Market_Share], Address=[Address], Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    width = 700
    height = 500

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортировнный по годам датафрейм

    pv = pd.pivot_table(  # создание сводной таблицы из текущего датафрейма
        df_plot,  # выбор текущего датафрейма
        index=['Year'],  # выбор индекса ("строки" в Excel Pivot Tables)
        columns=['Agency'],  # выбор столбцов ("столбцы" в Excel Pivot Tables)
        values=["SQM"],  # выбор подсчитываемого значения ("значения" в Excel Pivot Tables)
        aggfunc=sum,  # параметр поля значения (сумма, кол-во, среднее итд)
        fill_value=0)  # заполнение пустых ячеек

    if len(df_plot['Agency'].unique()) == 6:
        colliers_sum = (((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64))
        cw_sum = (((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64))
        cbre_sum = (((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64))
        jll_sum = (((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64))
        kf_sum = (((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64))
        sar_sum = (((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64))
        data = []
        annotations = []
        trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                        name='Colliers',
                        marker=dict(
                            color=color.colliers_dark_blue),
                        width=0.4,
                        text=list(colliers_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                        name='CW',
                        marker=dict(
                            color=color.colliers_extra_light_blue),
                        width=0.4,
                        text=list(cw_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                        name='CBRE',
                        marker=dict(
                            color=color.colliers_grey_40),
                        width=0.4,
                        text=list(cbre_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                        name='JLL',
                        marker=dict(
                            color=color.colliers_yellow),
                        width=0.4,
                        text=list(jll_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12))

        trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                        name='KF',
                        marker=dict(
                            color=color.colliers_red),
                        width=0.4,
                        text=list(kf_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))

        trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                        name='SAR',
                        marker=dict(
                            color=color.colliers_light_blue),
                        width=0.4,
                        text=list(sar_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))

        # добавление подписи на графике по центру трейса
        for year, value in zip(pv.index, colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex in zip(pv.index, cw_sum, colliers_sum):
            annotations.append(dict(
                x=year,
                y=value_ex * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex, value_ex_ex in zip(pv.index, cbre_sum, cw_sum, colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex) * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex, value_ex_ex, value_ex_ex_ex in zip(pv.index, jll_sum, cbre_sum, cw_sum,
                                                                      colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex + value_ex_ex_ex) * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.colliers_grey_80),
            )
            )

        for year, value, value_ex, value_ex_ex, value_ex_ex_ex, value_ex_ex_ex_ex in zip(pv.index, kf_sum, jll_sum,
                                                                                         cbre_sum, cw_sum,
                                                                                         colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex + value_ex_ex_ex + value_ex_ex_ex_ex) * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex, value_ex_ex, value_ex_ex_ex, value_ex_ex_ex_ex, value_ex_ex_ex_ex_ex in zip(pv.index,
                                                                                                               sar_sum,
                                                                                                               kf_sum,
                                                                                                               jll_sum,
                                                                                                               cbre_sum,
                                                                                                               cw_sum,
                                                                                                               colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex + value_ex_ex_ex + value_ex_ex_ex_ex + value_ex_ex_ex_ex_ex) * 1000 + (
                        value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])

    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        annotations = []
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                            name='Colliers',
                            marker=dict(
                                color=color.colliers_dark_blue),
                            width=0.4,
                            text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace1)

        if 'CW' in list_of_unique:
            trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                            name='CW',
                            marker=dict(
                                color=color.colliers_extra_light_blue),
                            width=0.4,
                            text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace2)

        if 'CBRE' in list_of_unique:
            trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                            name='CBRE',
                            marker=dict(
                                color=color.colliers_grey_40),
                            width=0.4,
                            text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace3)

        if 'JLL' in list_of_unique:
            trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                            name='JLL',
                            marker=dict(
                                color=color.colliers_yellow),
                            width=0.4,
                            text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.colliers_grey_80,
                                size=12))
            data.append(trace4)

        if 'KF' in list_of_unique:
            trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                            name='KF',
                            marker=dict(
                                color=color.colliers_red),
                            width=0.4,
                            text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace5)

        if 'SAR' in list_of_unique:
            trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                            name='SAR',
                            marker=dict(
                                color=color.colliers_light_blue),
                            width=0.4,
                            text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))

            data.append(trace6)

    # '''
    #     Формирование строки для подписи графика
    #     Сначала создаётся лист со значениями выбранных индексов для фильтрации
    #     Если парметры не выбраны, то выводится 'All deals' и 'All years'
    #     Если парметры выбраны, и не указан год, то выводятся элементы списка значений
    #     выбранных параметров и 'All years'
    #     Если парметры выбраны и указан год, то выводятся элементы списка значений
    #     выбранных параметров и элементы списка 'Year'
    #                                                                                    '''

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    return {
        'data': data,
        'layout':
            go.Layout(
                title='{}<br>'
                      'in {}'.format(format_data, format_year),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=12),
                width=width,
                height=height,
                margin=dict(pad=0),
                titlefont=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=18),
                xaxis=dict(
                    exponentformat=False,
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=False,
                    ticks='',
                    showticklabels=True,
                    # title='Years'
                ),
                yaxis={'title': 'Area in sq.m'},
                legend=dict(orientation="h",
                            traceorder="normal"),
                barmode='stack',
                annotations=annotations
            )
    }

