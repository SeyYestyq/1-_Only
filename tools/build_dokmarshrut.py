# -*- coding: utf-8 -*-
"""Сборка выгрузки конфигурации «ДокМаршрут» (XML 2.17)."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cf_common import (  # noqa: E402
    FormBuilder,
    style_item_xml,
    Writer,
    attribute_xml,
    column_xml,
    esc,
    form_file,
    generated,
    register_field,
    syn,
    tabular_section,
    type_bool,
    type_date,
    type_number,
    type_ref,
    type_string,
    uid,
    wrap,
)
from build_configurations import (  # noqa: E402
    catalog_xml,
    configuration_xml,
    constant_xml,
    enum_xml,
    language_xml,
    module_xml,
    processor_xml,
    rights_xml,
    role_xml,
    subsystem_xml,
    template_meta,
)

ROOT = Path(__file__).resolve().parents[1]
BSL = ROOT / "tools" / "bsl" / "dokmarshrut"


def read_bsl(relative: str) -> str:
    return (BSL / relative).read_text(encoding="utf-8")


def save_module(writer: Writer, relative_xml_body, xml_path, bsl_path, bsl_relative):
    writer.xml(xml_path, relative_xml_body)
    writer.bsl(bsl_path, read_bsl(bsl_relative))


def save_form(writer: Writer, folder, object_name, form_name, synonym, form_xml, bsl_relative):
    descriptor, layout = form_file(f"{folder}/{object_name}/{form_name}", form_name, synonym, form_xml)
    base = f"{folder}/{object_name}/Forms/{form_name}"
    writer.raw(base + ".xml", descriptor)
    writer.raw(base + "/Ext/Form.xml", layout)
    writer.bsl(base + "/Ext/Form/Module.bsl", read_bsl(bsl_relative))


def type_enum(enum_name: str) -> str:
    return f"<Type><v8:Type>cfg:EnumRef.{enum_name}</v8:Type></Type>"


def catalog_list_form_xml(main_table: str, columns, help_button: bool = False, yellow_create: bool = False) -> str:
    """Простой список справочника (DynamicList)."""
    fields = []
    nid = 10
    for name, path in columns:
        fields.append(
            f'<LabelField name="{name}" id="{nid}">'
            f"<DataPath>{path}</DataPath>"
            f'<ContextMenu name="{name}КонтекстноеМеню" id="{nid + 1}"/>'
            f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{nid + 2}"/>'
            "</LabelField>"
        )
        nid += 3
    buttons = []
    commands = []
    if yellow_create:
        buttons.append(
            '<Button name="КнопкаСоздать" id="100">'
            "<Type>CommandBarButton</Type><DefaultButton>true</DefaultButton>"
            "<CommandName>Form.Command.Создать</CommandName>"
            '<ExtendedTooltip name="КнопкаСоздатьРасширеннаяПодсказка" id="101"/>'
            "</Button>"
        )
        commands.append(
            """<Command name="Создать" id="102">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Создать</v8:content></v8:item></Title>
<Action>Создать</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>"""
        )
    if help_button:
        buttons.append(
            '<Button name="КнопкаИнструкция" id="60">'
            "<Type>CommandBarButton</Type><Representation>Picture</Representation>"
            "<CommandName>Form.Command.ПоказатьИнструкцию</CommandName>"
            '<ExtendedTooltip name="КнопкаИнструкцияРасширеннаяПодсказка" id="61"/>'
            "</Button>"
        )
        commands.append(
            """<Command name="ПоказатьИнструкцию" id="62">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Справка</v8:content></v8:item></Title>
<ToolTip><v8:item><v8:lang>ru</v8:lang><v8:content>Справка по списку</v8:content></v8:item></ToolTip>
<Picture><xr:Ref>StdPicture.Information</xr:Ref><xr:LoadTransparent>true</xr:LoadTransparent></Picture>
<Action>ПоказатьИнструкцию</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>"""
        )
    bar_extra = f"<ChildItems>{''.join(buttons)}</ChildItems>" if buttons else ""
    commands_xml = f"<Commands>{''.join(commands)}</Commands>" if commands else ""
    command_set = (
        "<CommandSet><ExcludedCommand>Create</ExcludedCommand></CommandSet>"
        if yellow_create
        else ""
    )
    return f"""<WindowOpeningMode>Independent</WindowOpeningMode>
<AutoTitle>true</AutoTitle>
{command_set}
<AutoCommandBar name="ФормаКоманднаяПанель" id="-1"><Autofill>true</Autofill>{bar_extra}</AutoCommandBar>
<Events><Event name="OnCreateAtServer">ПриСозданииНаСервере</Event></Events>
<ChildItems>
<Table name="Список" id="1">
<Representation>List</Representation>
<CommandBarLocation>None</CommandBarLocation>
<DefaultItem>true</DefaultItem>
<UseAlternationRowColor>true</UseAlternationRowColor>
<DataPath>Список</DataPath>
<RowPictureDataPath>Список.DefaultPicture</RowPictureDataPath>
<AutoRefresh>false</AutoRefresh>
<AutoRefreshPeriod>60</AutoRefreshPeriod>
<Period>
<v8:variant xsi:type="v8:StandardPeriodVariant">Custom</v8:variant>
<v8:startDate>0001-01-01T00:00:00</v8:startDate>
<v8:endDate>0001-01-01T00:00:00</v8:endDate>
</Period>
<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>
<RestoreCurrentRow>false</RestoreCurrentRow>
<TopLevelParent xsi:nil="true"/>
<ShowRoot>true</ShowRoot>
<AllowRootChoice>false</AllowRootChoice>
<UpdateOnDataChange>Auto</UpdateOnDataChange>
<AllowGettingCurrentRowURL>true</AllowGettingCurrentRowURL>
<ContextMenu name="СписокКонтекстноеМеню" id="2"/>
<AutoCommandBar name="СписокКоманднаяПанель" id="3"><Autofill>true</Autofill></AutoCommandBar>
<ExtendedTooltip name="СписокРасширеннаяПодсказка" id="4"/>
<SearchStringAddition name="СписокСтрокаПоиска" id="5"><AdditionSource><Item>Список</Item><Type>SearchStringRepresentation</Type></AdditionSource><ContextMenu name="СписокСтрокаПоискаКонтекстноеМеню" id="6"/><ExtendedTooltip name="СписокСтрокаПоискаРасширеннаяПодсказка" id="7"/></SearchStringAddition>
<ViewStatusAddition name="СписокСостояниеПросмотра" id="8"><AdditionSource><Item>Список</Item><Type>ViewStatusRepresentation</Type></AdditionSource><ContextMenu name="СписокСостояниеПросмотраКонтекстноеМеню" id="9"/><ExtendedTooltip name="СписокСостояниеПросмотраРасширеннаяПодсказка" id="55"/></ViewStatusAddition>
<SearchControlAddition name="СписокУправлениеПоиском" id="56"><AdditionSource><Item>Список</Item><Type>SearchControl</Type></AdditionSource><ContextMenu name="СписокУправлениеПоискомКонтекстноеМеню" id="57"/><ExtendedTooltip name="СписокУправлениеПоискомРасширеннаяПодсказка" id="58"/></SearchControlAddition>
<ChildItems>{''.join(fields)}</ChildItems>
</Table>
</ChildItems>
<Attributes>
<Attribute name="Список" id="59">
<Type><v8:Type>cfg:DynamicList</v8:Type></Type>
<MainAttribute>true</MainAttribute>
<Settings xsi:type="DynamicList"><ManualQuery>false</ManualQuery><DynamicDataRead>true</DynamicDataRead><MainTable>{main_table}</MainTable><ListSettings/></Settings>
</Attribute>
</Attributes>
{commands_xml}"""


def document_list_form_xml() -> str:
    """Список ДокументСЭД: 4 быстрых отбора + DynamicList + «Мои задачи»."""
    columns = [
        ("Номер", "Список.Number"),
        ("Дата", "Список.Date"),
        ("Категория", "Список.Категория"),
        ("ВидДокумента", "Список.ВидДокумента"),
        ("Ответственный", "Список.Ответственный"),
        ("Статус", "Список.Статус"),
        ("ТекущийСогласующий", "Список.ТекущийСогласующий"),
        ("ТекущийЭтап", "Список.ТекущийЭтап"),
    ]
    fields = []
    nid = 10
    for name, path in columns:
        fields.append(
            f'<LabelField name="{name}" id="{nid}">'
            f"<DataPath>{path}</DataPath>"
            f'<ContextMenu name="{name}КонтекстноеМеню" id="{nid + 1}"/>'
            f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{nid + 2}"/>'
            "</LabelField>"
        )
        nid += 3

    filter_fields = (
        _filter_input("ОтборКатегория", "ОтборКатегория", "ОтборПриИзменении", 70)
        + _filter_input("ОтборВидДокумента", "ОтборВидДокумента", "ОтборПриИзменении", 73)
        + _filter_input("ОтборОтветственный", "ОтборОтветственный", "ОтборПриИзменении", 76)
        + _filter_input("ОтборСтатус", "ОтборСтатус", "ОтборПриИзменении", 79)
        + _filter_reset_button(88)
    )

    return f"""<WindowOpeningMode>Independent</WindowOpeningMode>
<AutoTitle>true</AutoTitle>
<CommandSet>
<ExcludedCommand>Create</ExcludedCommand>
</CommandSet>
<AutoCommandBar name="ФормаКоманднаяПанель" id="-1"><Autofill>true</Autofill><ChildItems><Button name="КнопкаСоздать" id="100"><Type>CommandBarButton</Type><DefaultButton>true</DefaultButton><CommandName>Form.Command.СоздатьДокумент</CommandName><ExtendedTooltip name="КнопкаСоздатьРасширеннаяПодсказка" id="101"/></Button><Button name="КнопкаИнструкция" id="60"><Type>CommandBarButton</Type><Representation>Picture</Representation><CommandName>Form.Command.ПоказатьИнструкцию</CommandName><ExtendedTooltip name="КнопкаИнструкцияРасширеннаяПодсказка" id="61"/></Button><Button name="КнопкаМои" id="53"><Type>CommandBarButton</Type><CommandName>Form.Command.ПоказатьТолькоМоиСогласования</CommandName><ExtendedTooltip name="КнопкаМоиРасширеннаяПодсказка" id="54"/></Button></ChildItems></AutoCommandBar>
<Events><Event name="OnCreateAtServer">ПриСозданииНаСервере</Event></Events>
<ChildItems>
<UsualGroup name="ГруппаОтборы" id="82">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Быстрые отборы</v8:content></v8:item></Title>
<Group>Horizontal</Group>
<Representation>None</Representation>
<ShowTitle>false</ShowTitle>
<ExtendedTooltip name="ГруппаОтборыРасширеннаяПодсказка" id="83"/>
<ChildItems>{filter_fields}</ChildItems>
</UsualGroup>
<Table name="Список" id="1">
<Representation>List</Representation>
<CommandBarLocation>None</CommandBarLocation>
<DefaultItem>true</DefaultItem>
<UseAlternationRowColor>true</UseAlternationRowColor>
<EnableStartDrag>false</EnableStartDrag>
<DataPath>Список</DataPath>
<RowPictureDataPath>Список.DefaultPicture</RowPictureDataPath>
<AutoRefresh>false</AutoRefresh>
<AutoRefreshPeriod>60</AutoRefreshPeriod>
<Period>
<v8:variant xsi:type="v8:StandardPeriodVariant">Custom</v8:variant>
<v8:startDate>0001-01-01T00:00:00</v8:startDate>
<v8:endDate>0001-01-01T00:00:00</v8:endDate>
</Period>
<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>
<RestoreCurrentRow>false</RestoreCurrentRow>
<TopLevelParent xsi:nil="true"/>
<ShowRoot>true</ShowRoot>
<AllowRootChoice>false</AllowRootChoice>
<UpdateOnDataChange>Auto</UpdateOnDataChange>
<AllowGettingCurrentRowURL>true</AllowGettingCurrentRowURL>
<ContextMenu name="СписокКонтекстноеМеню" id="2"/>
<AutoCommandBar name="СписокКоманднаяПанель" id="3"><Autofill>true</Autofill></AutoCommandBar>
<ExtendedTooltip name="СписокРасширеннаяПодсказка" id="4"/>
<SearchStringAddition name="СписокСтрокаПоиска" id="5">
<AdditionSource><Item>Список</Item><Type>SearchStringRepresentation</Type></AdditionSource>
<ContextMenu name="СписокСтрокаПоискаКонтекстноеМеню" id="6"/>
<ExtendedTooltip name="СписокСтрокаПоискаРасширеннаяПодсказка" id="7"/>
</SearchStringAddition>
<ViewStatusAddition name="СписокСостояниеПросмотра" id="8">
<AdditionSource><Item>Список</Item><Type>ViewStatusRepresentation</Type></AdditionSource>
<ContextMenu name="СписокСостояниеПросмотраКонтекстноеМеню" id="48"/>
<ExtendedTooltip name="СписокСостояниеПросмотраРасширеннаяПодсказка" id="49"/>
</ViewStatusAddition>
<SearchControlAddition name="СписокУправлениеПоиском" id="9">
<AdditionSource><Item>Список</Item><Type>SearchControl</Type></AdditionSource>
<ContextMenu name="СписокУправлениеПоискомКонтекстноеМеню" id="50"/>
<ExtendedTooltip name="СписокУправлениеПоискомРасширеннаяПодсказка" id="51"/>
</SearchControlAddition>
<ChildItems>{''.join(fields)}</ChildItems>
</Table>
</ChildItems>
<Attributes>
<Attribute name="Список" id="52">
<Type><v8:Type>cfg:DynamicList</v8:Type></Type>
<MainAttribute>true</MainAttribute>
<Settings xsi:type="DynamicList">
<ManualQuery>false</ManualQuery>
<DynamicDataRead>true</DynamicDataRead>
<QueryText/>
<MainTable>Document.ДокументСЭД</MainTable>
<ListSettings>
<dcsset:filter>
<dcsset:viewMode>Normal</dcsset:viewMode>
<dcsset:userSettingID>a0000000-0000-0000-0000-000000000001</dcsset:userSettingID>
</dcsset:filter>
<dcsset:order>
<dcsset:viewMode>Normal</dcsset:viewMode>
<dcsset:userSettingID>a0000000-0000-0000-0000-000000000002</dcsset:userSettingID>
</dcsset:order>
<dcsset:conditionalAppearance>
<dcsset:viewMode>Normal</dcsset:viewMode>
<dcsset:userSettingID>a0000000-0000-0000-0000-000000000003</dcsset:userSettingID>
</dcsset:conditionalAppearance>
<dcsset:itemsViewMode>Normal</dcsset:itemsViewMode>
<dcsset:itemsUserSettingID>a0000000-0000-0000-0000-000000000004</dcsset:itemsUserSettingID>
</ListSettings>
</Settings>
</Attribute>
<Attribute name="ТолькоМоиСогласования" id="55">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Только мои согласования</v8:content></v8:item></Title>
<Type><v8:Type>xs:boolean</v8:Type></Type>
</Attribute>
<Attribute name="ТолькоМоиДокументы" id="105">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Только мои документы</v8:content></v8:item></Title>
<Type><v8:Type>xs:boolean</v8:Type></Type>
</Attribute>
<Attribute name="ОтборКатегория" id="84">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Категория</v8:content></v8:item></Title>
{type_enum("КатегорииДокументов")}
</Attribute>
<Attribute name="ОтборВидДокумента" id="85">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Вид документа</v8:content></v8:item></Title>
{type_ref("CatalogRef.ВидыДокументов")}
</Attribute>
<Attribute name="ОтборОтветственный" id="86">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Ответственный</v8:content></v8:item></Title>
{type_ref("CatalogRef.Сотрудники")}
</Attribute>
<Attribute name="ОтборСтатус" id="87">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Статус</v8:content></v8:item></Title>
{type_enum("СтатусыДокументов")}
</Attribute>
</Attributes>
<Commands>
<Command name="СоздатьДокумент" id="102">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Создать</v8:content></v8:item></Title>
<Action>СоздатьДокумент</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>
<Command name="ПоказатьИнструкцию" id="62">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Справка</v8:content></v8:item></Title>
<ToolTip><v8:item><v8:lang>ru</v8:lang><v8:content>Справка: список документов</v8:content></v8:item></ToolTip>
<Picture><xr:Ref>StdPicture.Information</xr:Ref><xr:LoadTransparent>true</xr:LoadTransparent></Picture>
<Action>ПоказатьИнструкцию</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>
<Command name="ПоказатьТолькоМоиСогласования" id="56">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Мои задачи</v8:content></v8:item></Title>
<ToolTip/><Action>ПоказатьТолькоМоиСогласования</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>
{_reset_filters_command_xml(90)}
</Commands>
<Parameters>
<Parameter name="ПоказатьМоиДокументы"><Type><v8:Type>xs:boolean</v8:Type></Type></Parameter>
<Parameter name="ПоказатьМоиСогласования"><Type><v8:Type>xs:boolean</v8:Type></Type></Parameter>
</Parameters>"""


def document_xml_no_posting(name, synonym, attributes, tabular_xml, forms, templates, object_form):
    internal = generated([
        (f"DocumentObject.{name}", "Object", name + ".obj"),
        (f"DocumentRef.{name}", "Ref", name + ".ref"),
        (f"DocumentSelection.{name}", "Selection", name + ".sel"),
        (f"DocumentList.{name}", "List", name + ".list"),
        (f"DocumentManager.{name}", "Manager", name + ".man"),
    ])
    form_refs = "".join(f"<Form>{form_name}</Form>" for form_name in forms)
    template_refs = "".join(f"<Template>{template_name}</Template>" for template_name in templates)
    return f"""<Document uuid="{uid('doc:' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<UseStandardCommands>true</UseStandardCommands>
<Numerator/>
<NumberType>String</NumberType>
<NumberLength>11</NumberLength>
<NumberAllowedLength>Variable</NumberAllowedLength>
<NumberPeriodicity>Nonperiodical</NumberPeriodicity>
<CheckUnique>true</CheckUnique>
<Autonumbering>true</Autonumbering>
<Characteristics/>
<BasedOn/>
<InputByString>
<xr:Field>Document.{name}.StandardAttribute.Number</xr:Field>
</InputByString>
<CreateOnInput>Use</CreateOnInput>
<SearchStringModeOnInputByString>Begin</SearchStringModeOnInputByString>
<FullTextSearchOnInputByString>DontUse</FullTextSearchOnInputByString>
<ChoiceDataGetModeOnInputByString>Directly</ChoiceDataGetModeOnInputByString>
<DefaultObjectForm>Document.{name}.Form.{object_form}</DefaultObjectForm>
<DefaultListForm>Document.{name}.Form.ФормаСписка</DefaultListForm>
<DefaultChoiceForm/>
<AuxiliaryObjectForm/>
<AuxiliaryListForm/>
<AuxiliaryChoiceForm/>
<Posting>Deny</Posting>
<RealTimePosting>Deny</RealTimePosting>
<RegisterRecordsDeletion>AutoDeleteOnUnpost</RegisterRecordsDeletion>
<RegisterRecordsWritingOnPost>WriteSelected</RegisterRecordsWritingOnPost>
<SequenceFilling>AutoFillOff</SequenceFilling>
<RegisterRecords/>
<PostInPrivilegedMode>true</PostInPrivilegedMode>
<UnpostInPrivilegedMode>true</UnpostInPrivilegedMode>
<IncludeHelpInContents>false</IncludeHelpInContents>
<DataLockFields/>
<DataLockControlMode>Managed</DataLockControlMode>
<FullTextSearch>Use</FullTextSearch>
<ObjectPresentation><v8:item><v8:lang>ru</v8:lang><v8:content>Документ</v8:content></v8:item></ObjectPresentation>
<ExtendedObjectPresentation/>
<ListPresentation><v8:item><v8:lang>ru</v8:lang><v8:content>Список документов</v8:content></v8:item></ListPresentation>
<ExtendedListPresentation/>
<Explanation/>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
<DataHistory>DontUse</DataHistory>
<UpdateDataHistoryImmediatelyAfterWrite>false</UpdateDataHistoryImmediatelyAfterWrite>
<ExecuteAfterWriteDataHistoryVersionProcessing>false</ExecuteAfterWriteDataHistoryVersionProcessing>
</Properties>
<ChildObjects>
{''.join(attributes)}
{form_refs}
{tabular_xml}
{template_refs}
</ChildObjects>
</Document>"""


def information_register_xml(name, synonym, dimensions, resources, list_form=""):
    internal = generated([
        (f"InformationRegisterRecord.{name}", "Record", name + ".rec"),
        (f"InformationRegisterManager.{name}", "Manager", name + ".man"),
        (f"InformationRegisterSelection.{name}", "Selection", name + ".sel"),
        (f"InformationRegisterList.{name}", "List", name + ".list"),
        (f"InformationRegisterRecordSet.{name}", "RecordSet", name + ".set"),
        (f"InformationRegisterRecordKey.{name}", "RecordKey", name + ".key"),
        (f"InformationRegisterRecordManager.{name}", "RecordManager", name + ".recman"),
    ])
    default_list = (
        f"<DefaultListForm>InformationRegister.{name}.Form.{list_form}</DefaultListForm>"
        if list_form
        else "<DefaultListForm/>"
    )
    form_ref = f"<Form>{list_form}</Form>" if list_form else ""
    return f"""<InformationRegister uuid="{uid('ireg:' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<UseStandardCommands>true</UseStandardCommands>
<EditType>InDialog</EditType>
<DefaultRecordForm/>
{default_list}
<AuxiliaryRecordForm/>
<AuxiliaryListForm/>
<InformationRegisterPeriodicity>Nonperiodical</InformationRegisterPeriodicity>
<WriteMode>Independent</WriteMode>
<MainFilterOnPeriod>false</MainFilterOnPeriod>
<IncludeHelpInContents>false</IncludeHelpInContents>
<DataLockControlMode>Managed</DataLockControlMode>
<FullTextSearch>DontUse</FullTextSearch>
<EnableTotalsSliceFirst>false</EnableTotalsSliceFirst>
<EnableTotalsSliceLast>false</EnableTotalsSliceLast>
<RecordPresentation/>
<ExtendedRecordPresentation/>
<ListPresentation/>
<ExtendedListPresentation/>
<Explanation/>
<DataHistory>DontUse</DataHistory>
<UpdateDataHistoryImmediatelyAfterWrite>false</UpdateDataHistoryImmediatelyAfterWrite>
<ExecuteAfterWriteDataHistoryVersionProcessing>false</ExecuteAfterWriteDataHistoryVersionProcessing>
</Properties>
<ChildObjects>
{''.join(dimensions)}
{''.join(resources)}
{form_ref}
</ChildObjects>
</InformationRegister>"""


def register_list_form_xml(main_table: str, columns, help_button: bool = True) -> str:
    """Список регистра только для просмотра (без «+»)."""
    return _list_form_xml(
        main_table,
        columns,
        help_button=help_button,
        help_tooltip="Справка: журнал уведомлений",
        read_only=True,
        autofill_bar=False,
        filters_xml="",
        filter_attrs_xml="",
    )


def journal_list_form_xml() -> str:
    """Журнал уведомлений: быстрые отборы Документ / Получатель / Событие / Только ошибки."""
    columns = [
        ("Документ", "Список.Документ"),
        ("ДатаВремя", "Список.ДатаВремя"),
        ("Получатель", "Список.Получатель"),
        ("Событие", "Список.Событие"),
        ("Успешно", "Список.Успешно"),
        ("ТекстОшибки", "Список.ТекстОшибки"),
    ]
    filters = (
        _filter_input("ОтборДокумент", "ОтборДокумент", "ОтборПриИзменении", 70)
        + _filter_input("ОтборПолучатель", "ОтборПолучатель", "ОтборПриИзменении", 73)
        + _filter_input("ОтборСобытие", "ОтборСобытие", "ОтборПриИзменении", 76)
        + _filter_checkbox("ОтборТолькоОшибки", "ОтборТолькоОшибки", "ОтборПриИзменении", 79)
        + _filter_reset_button(88)
        + (
            '<Button name="КнопкаПовторить" id="91">'
            "<Type>UsualButton</Type>"
            '<CommandName>Form.Command.ПовторитьОтправку</CommandName>'
            '<ExtendedTooltip name="КнопкаПовторитьРасширеннаяПодсказка" id="92"/>'
            "</Button>"
        )
    )
    filter_attrs = f"""
<Attribute name="ОтборДокумент" id="84">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Документ</v8:content></v8:item></Title>
{type_ref("DocumentRef.ДокументСЭД")}
</Attribute>
<Attribute name="ОтборПолучатель" id="85">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Получатель</v8:content></v8:item></Title>
{type_string(150)}
</Attribute>
<Attribute name="ОтборСобытие" id="86">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Событие</v8:content></v8:item></Title>
{type_string(100)}
</Attribute>
<Attribute name="ОтборТолькоОшибки" id="87">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Только ошибки</v8:content></v8:item></Title>
{type_bool()}
</Attribute>"""
    return _list_form_xml(
        "InformationRegister.ЖурналУведомлений",
        columns,
        help_button=True,
        help_tooltip="Справка: журнал уведомлений",
        # Как у списка документов: выбор строк + «⋯» с удалением записей журнала.
        read_only=False,
        autofill_bar=True,
        exclude_create=True,
        filters_xml=filters,
        filter_attrs_xml=filter_attrs,
        extra_commands_xml="""
<Command name="ПовторитьОтправку" id="93">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Отправить повторно</v8:content></v8:item></Title>
<ToolTip><v8:item><v8:lang>ru</v8:lang><v8:content>Повторить выбранную неудачную отправку</v8:content></v8:item></ToolTip>
<Action>ПовторитьОтправку</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>""",
    )


def kinds_list_form_xml() -> str:
    """Список видов: отборы Категория / Статус настройки."""
    columns = [
        ("Наименование", "Список.Description"),
        ("Категория", "Список.Категория"),
        ("Префикс", "Список.Префикс"),
        ("СтатусНастройки", "Список.СтатусНастройки"),
    ]
    filters = (
        _filter_input("ОтборКатегория", "ОтборКатегория", "ОтборПриИзменении", 70)
        + _filter_input("ОтборСтатусНастройки", "ОтборСтатусНастройки", "ОтборПриИзменении", 73)
        + _filter_reset_button(88)
    )
    filter_attrs = f"""
<Attribute name="ОтборКатегория" id="84">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Категория</v8:content></v8:item></Title>
{type_enum("КатегорииДокументов")}
</Attribute>
<Attribute name="ОтборСтатусНастройки" id="85">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Статус настройки</v8:content></v8:item></Title>
{type_enum("СтатусыНастройкиВида")}
</Attribute>"""
    return _list_form_xml(
        "Catalog.ВидыДокументов",
        columns,
        help_button=True,
        help_tooltip="Справка: виды документов",
        read_only=False,
        autofill_bar=True,
        filters_xml=filters,
        filter_attrs_xml=filter_attrs,
        extra_bar_buttons=(
            '<Button name="КнопкаМастер" id="94">'
            "<Type>CommandBarButton</Type>"
            "<DefaultButton>true</DefaultButton>"
            "<CommandName>Form.Command.СоздатьВМастере</CommandName>"
            '<ExtendedTooltip name="КнопкаМастерРасширеннаяПодсказка" id="95"/>'
            "</Button>"
        ),
        extra_commands_xml="""
<Command name="СоздатьВМастере" id="96">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Создать</v8:content></v8:item></Title>
<Action>СоздатьВМастере</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>""",
        exclude_create=True,
    )


def _filter_input(name: str, path: str, event: str, iid: int) -> str:
    return (
        f'<InputField name="{name}" id="{iid}">'
        f"<DataPath>{path}</DataPath>"
        "<TitleLocation>Top</TitleLocation>"
        "<Width>14</Width>"
        "<AutoMaxWidth>false</AutoMaxWidth>"
        "<ClearButton>true</ClearButton>"
        f'<Events><Event name="OnChange">{event}</Event></Events>'
        f'<ContextMenu name="{name}КонтекстноеМеню" id="{iid + 1}"/>'
        f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{iid + 2}"/>'
        "</InputField>"
    )


def _filter_checkbox(name: str, path: str, event: str, iid: int) -> str:
    return (
        f'<CheckBoxField name="{name}" id="{iid}">'
        f"<DataPath>{path}</DataPath>"
        "<TitleLocation>Right</TitleLocation>"
        "<CheckBoxType>Auto</CheckBoxType>"
        f'<Events><Event name="OnChange">{event}</Event></Events>'
        f'<ContextMenu name="{name}КонтекстноеМеню" id="{iid + 1}"/>'
        f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{iid + 2}"/>'
        "</CheckBoxField>"
    )


def _filter_reset_button(iid: int) -> str:
    return (
        f'<Button name="КнопкаСброситьОтборы" id="{iid}">'
        "<Type>UsualButton</Type>"
        '<CommandName>Form.Command.СброситьОтборы</CommandName>'
        f'<ExtendedTooltip name="КнопкаСброситьОтборыРасширеннаяПодсказка" id="{iid + 1}"/>'
        "</Button>"
    )


def _reset_filters_command_xml(cmd_id: int = 90) -> str:
    return f"""
<Command name="СброситьОтборы" id="{cmd_id}">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Сбросить</v8:content></v8:item></Title>
<ToolTip><v8:item><v8:lang>ru</v8:lang><v8:content>Очистить быстрые отборы</v8:content></v8:item></ToolTip>
<Action>СброситьОтборы</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>"""


def _list_form_xml(
    main_table: str,
    columns,
    *,
    help_button: bool,
    help_tooltip: str,
    read_only: bool,
    autofill_bar: bool,
    filters_xml: str,
    filter_attrs_xml: str,
    extra_commands_xml: str = "",
    extra_bar_buttons: str = "",
    exclude_create: bool = False,
) -> str:
    fields = []
    nid = 10
    for name, path in columns:
        fields.append(
            f'<LabelField name="{name}" id="{nid}">'
            f"<DataPath>{path}</DataPath>"
            f'<ContextMenu name="{name}КонтекстноеМеню" id="{nid + 1}"/>'
            f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{nid + 2}"/>'
            "</LabelField>"
        )
        nid += 3
    bar_extra = ""
    command_items = []
    help_button_xml = ""
    if help_button:
        help_button_xml = (
            '<Button name="КнопкаИнструкция" id="60">'
            "<Type>CommandBarButton</Type><Representation>Picture</Representation>"
            '<CommandName>Form.Command.ПоказатьИнструкцию</CommandName>'
            '<ExtendedTooltip name="КнопкаИнструкцияРасширеннаяПодсказка" id="61"/>'
            "</Button>"
        )
    if help_button or extra_bar_buttons:
        bar_extra = "<ChildItems>" + help_button_xml + extra_bar_buttons + "</ChildItems>"
        command_items.append(
            f"""<Command name="ПоказатьИнструкцию" id="62">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Справка</v8:content></v8:item></Title>
<ToolTip><v8:item><v8:lang>ru</v8:lang><v8:content>{esc(help_tooltip)}</v8:content></v8:item></ToolTip>
<Picture><xr:Ref>StdPicture.Information</xr:Ref><xr:LoadTransparent>true</xr:LoadTransparent></Picture>
<Action>ПоказатьИнструкцию</Action>
<CurrentRowUse>DontUse</CurrentRowUse>
</Command>"""
        )
    if filters_xml:
        command_items.append(_reset_filters_command_xml(90))
    if extra_commands_xml:
        command_items.append(extra_commands_xml)
    commands_xml = f"<Commands>{''.join(command_items)}</Commands>" if command_items else ""
    filters_block = ""
    if filters_xml:
        filters_block = f"""
<UsualGroup name="ГруппаОтборы" id="82">
<Title><v8:item><v8:lang>ru</v8:lang><v8:content>Быстрые отборы</v8:content></v8:item></Title>
<Group>Horizontal</Group>
<Representation>None</Representation>
<ShowTitle>false</ShowTitle>
<ExtendedTooltip name="ГруппаОтборыРасширеннаяПодсказка" id="83"/>
<ChildItems>{filters_xml}</ChildItems>
</UsualGroup>"""
    ro = (
        "<ReadOnly>true</ReadOnly><ChangeRowSet>false</ChangeRowSet><ChangeRowOrder>false</ChangeRowOrder>"
        if read_only
        else ""
    )
    autofill = "true" if autofill_bar else "false"
    command_set = (
        "<CommandSet>\n<ExcludedCommand>Create</ExcludedCommand>\n</CommandSet>\n"
        if exclude_create
        else ""
    )
    return f"""<WindowOpeningMode>Independent</WindowOpeningMode>
<AutoTitle>true</AutoTitle>
{command_set}<AutoCommandBar name="ФормаКоманднаяПанель" id="-1"><Autofill>{autofill}</Autofill>{bar_extra}</AutoCommandBar>
<Events><Event name="OnCreateAtServer">ПриСозданииНаСервере</Event></Events>
<ChildItems>
{filters_block}
<Table name="Список" id="1">
<Representation>List</Representation>
<CommandBarLocation>None</CommandBarLocation>
{ro}
<DefaultItem>true</DefaultItem>
<UseAlternationRowColor>true</UseAlternationRowColor>
<DataPath>Список</DataPath>
<RowPictureDataPath>Список.DefaultPicture</RowPictureDataPath>
<AutoRefresh>false</AutoRefresh>
<AutoRefreshPeriod>60</AutoRefreshPeriod>
<Period>
<v8:variant xsi:type="v8:StandardPeriodVariant">Custom</v8:variant>
<v8:startDate>0001-01-01T00:00:00</v8:startDate>
<v8:endDate>0001-01-01T00:00:00</v8:endDate>
</Period>
<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>
<RestoreCurrentRow>false</RestoreCurrentRow>
<TopLevelParent xsi:nil="true"/>
<ShowRoot>true</ShowRoot>
<AllowRootChoice>false</AllowRootChoice>
<UpdateOnDataChange>Auto</UpdateOnDataChange>
<AllowGettingCurrentRowURL>true</AllowGettingCurrentRowURL>
<ContextMenu name="СписокКонтекстноеМеню" id="2"/>
<AutoCommandBar name="СписокКоманднаяПанель" id="3"><Autofill>{autofill}</Autofill></AutoCommandBar>
<ExtendedTooltip name="СписокРасширеннаяПодсказка" id="4"/>
<SearchStringAddition name="СписокСтрокаПоиска" id="5"><AdditionSource><Item>Список</Item><Type>SearchStringRepresentation</Type></AdditionSource><ContextMenu name="СписокСтрокаПоискаКонтекстноеМеню" id="6"/><ExtendedTooltip name="СписокСтрокаПоискаРасширеннаяПодсказка" id="7"/></SearchStringAddition>
<ViewStatusAddition name="СписокСостояниеПросмотра" id="8"><AdditionSource><Item>Список</Item><Type>ViewStatusRepresentation</Type></AdditionSource><ContextMenu name="СписокСостояниеПросмотраКонтекстноеМеню" id="9"/><ExtendedTooltip name="СписокСостояниеПросмотраРасширеннаяПодсказка" id="55"/></ViewStatusAddition>
<SearchControlAddition name="СписокУправлениеПоиском" id="56"><AdditionSource><Item>Список</Item><Type>SearchControl</Type></AdditionSource><ContextMenu name="СписокУправлениеПоискомКонтекстноеМеню" id="57"/><ExtendedTooltip name="СписокУправлениеПоискомРасширеннаяПодсказка" id="58"/></SearchControlAddition>
<ChildItems>{''.join(fields)}</ChildItems>
</Table>
</ChildItems>
<Attributes>
<Attribute name="Список" id="59">
<Type><v8:Type>cfg:DynamicList</v8:Type></Type>
<MainAttribute>true</MainAttribute>
<Settings xsi:type="DynamicList"><ManualQuery>false</ManualQuery><DynamicDataRead>true</DynamicDataRead><MainTable>{main_table}</MainTable><ListSettings/></Settings>
</Attribute>
{filter_attrs_xml}
</Attributes>
{commands_xml}"""


def ir_dimension(name, synonym, type_xml, key, deny=True):
    extra = (
        "<FillFromFillingValue>false</FillFromFillingValue>"
        "<FillValue xsi:nil=\"true\"/>"
        "<Master>false</Master>"
        "<MainFilter>true</MainFilter>"
        f"<DenyIncompleteValues>{'true' if deny else 'false'}</DenyIncompleteValues>"
        "<Indexing>DontIndex</Indexing>"
        "<FullTextSearch>Use</FullTextSearch>"
    )
    return register_field("Dimension", name, synonym, type_xml, key, extra)


def ir_resource(name, synonym, type_xml, key):
    extra = "<Indexing>DontIndex</Indexing><FullTextSearch>Use</FullTextSearch>"
    return register_field("Resource", name, synonym, type_xml, key, extra)


def sed_print_template():
    return """<?xml version="1.0" encoding="UTF-8"?>
<document xmlns="http://v8.1c.ru/8.2/data/spreadsheet" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<languageSettings>
<currentLanguage>ru</currentLanguage>
<defaultLanguage>ru</defaultLanguage>
<languageInfo><id>ru</id><code>Русский</code><description>Русский</description></languageInfo>
</languageSettings>
<columns>
<size>6</size>
<columnsItem><index>0</index><column><formatIndex>1</formatIndex></column></columnsItem>
<columnsItem><index>1</index><column><formatIndex>2</formatIndex></column></columnsItem>
<columnsItem><index>2</index><column><formatIndex>3</formatIndex></column></columnsItem>
<columnsItem><index>3</index><column><formatIndex>3</formatIndex></column></columnsItem>
<columnsItem><index>4</index><column><formatIndex>3</formatIndex></column></columnsItem>
<columnsItem><index>5</index><column><formatIndex>2</formatIndex></column></columnsItem>
</columns>
<rowsItem><index>0</index><row><c><c><f>4</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Документ [Номер] от [Дата]</v8:content></v8:item></tl></c></c></row></rowsItem>
<rowsItem><index>1</index><row><c><c><f>5</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Вид: [ВидДокумента] · Категория: [Категория] · Статус: [Статус]</v8:content></v8:item></tl></c></c></row></rowsItem>
<rowsItem><index>2</index><row><c><c><f>5</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Автор: [Автор] · Ответственный: [Ответственный] · Руководитель: [Руководитель] · Этап [ТекущийЭтап] из [ВсегоЭтапов]</v8:content></v8:item></tl></c></c></row></rowsItem>
<rowsItem><index>3</index><row><empty>true</empty></row></rowsItem>
<rowsItem><index>4</index><row>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Поле</v8:content></v8:item></tl></c></c>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Значение</v8:content></v8:item></tl></c></c>
</row></rowsItem>
<rowsItem><index>5</index><row>
<c><c><f>7</f><parameter>Заголовок</parameter></c></c>
<c><c><f>7</f><parameter>ЗначениеСтрока</parameter></c></c>
</row></rowsItem>
<rowsItem><index>6</index><row><empty>true</empty></row></rowsItem>
<rowsItem><index>7</index><row>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>№</v8:content></v8:item></tl></c></c>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Этап</v8:content></v8:item></tl></c></c>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Согласующий</v8:content></v8:item></tl></c></c>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Решение</v8:content></v8:item></tl></c></c>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Дата</v8:content></v8:item></tl></c></c>
<c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Комментарий</v8:content></v8:item></tl></c></c>
</row></rowsItem>
<rowsItem><index>8</index><row>
<c><c><f>7</f><parameter>НомерЭтапа</parameter></c></c>
<c><c><f>7</f><parameter>НазваниеЭтапа</parameter></c></c>
<c><c><f>7</f><parameter>Согласующий</parameter></c></c>
<c><c><f>7</f><parameter>Решение</parameter></c></c>
<c><c><f>7</f><parameter>ДатаРешения</parameter></c></c>
<c><c><f>7</f><parameter>Комментарий</parameter></c></c>
</row></rowsItem>
<rowsItem><index>9</index><row><c><c><f>5</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Сформировано ДокМаршрут</v8:content></v8:item></tl></c></c></row></rowsItem>
<templateMode>true</templateMode>
<defaultFormatIndex>8</defaultFormatIndex>
<height>10</height>
<vgRows>10</vgRows>
<merge><r>0</r><c>0</c><w>5</w></merge>
<merge><r>1</r><c>0</c><w>5</w></merge>
<merge><r>2</r><c>0</c><w>5</w></merge>
<merge><r>9</r><c>0</c><w>5</w></merge>
<namedItem xsi:type="NamedItemCells"><name>Шапка</name><area><type>Rows</type><beginRow>0</beginRow><endRow>3</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>ЗаголовокПолей</name><area><type>Rows</type><beginRow>4</beginRow><endRow>4</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>СтрокаПоля</name><area><type>Rows</type><beginRow>5</beginRow><endRow>5</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>ЗаголовокМаршрута</name><area><type>Rows</type><beginRow>7</beginRow><endRow>7</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>СтрокаМаршрута</name><area><type>Rows</type><beginRow>8</beginRow><endRow>8</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>Подвал</name><area><type>Rows</type><beginRow>9</beginRow><endRow>9</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<line width="1" gap="false"><v8ui:style xsi:type="v8ui:SpreadsheetDocumentCellLineType">Solid</v8ui:style></line>
<format><width>180</width></format>
<format><width>300</width></format>
<format><width>140</width></format>
<format><horizontalAlignment>Left</horizontalAlignment><textPlacement>Wrap</textPlacement><fillType>Template</fillType></format>
<format><horizontalAlignment>Left</horizontalAlignment><textPlacement>Wrap</textPlacement><fillType>Template</fillType></format>
<format><border>0</border><horizontalAlignment>Center</horizontalAlignment><fillType>Text</fillType></format>
<format><border>0</border><horizontalAlignment>Left</horizontalAlignment><fillType>Parameter</fillType></format>
<format><width>72</width></format>
</document>
"""


def build_dokmarshrut(root: Path):
    writer = Writer(root)
    name = "ДокМаршрут"
    style_defs = [
        ("АкцентПродукта", "Акцент продукта", "#FFDD00"),
        ("ТекстОсновной", "Текст основной", "#1C1C1F"),
        ("ТекстВторичный", "Текст вторичный", "#66666E"),
        ("СтатусЧерновикЦвет", "Статус черновик (текст)", "#4D4D54"),
        ("СтатусЧерновикФон", "Статус черновик (фон)", "#F5F5F5"),
        ("СтатусНаСогласованииЦвет", "Статус на согласовании (текст)", "#004DA1"),
        ("СтатусНаСогласованииФон", "Статус на согласовании (фон)", "#E5F2FF"),
        ("СтатусСогласованЦвет", "Статус согласован (текст)", "#01661A"),
        ("СтатусСогласованФон", "Статус согласован (фон)", "#E5FFEC"),
        ("СтатусОтклоненЦвет", "Статус отклонён (текст)", "#A11810"),
        ("СтатусОтклоненФон", "Статус отклонён (фон)", "#FFE7E5"),
        ("СтатусНаДоработкеЦвет", "Статус на доработке (текст)", "#704303"),
        ("СтатусНаДоработкеФон", "Статус на доработке (фон)", "#FFF4E5"),
    ]
    children = [
        ("Language", "Русский"),
        ("Subsystem", "Документы"),
        ("Subsystem", "Конструктор"),
        ("Subsystem", "Сотрудники"),
        ("Subsystem", "Уведомления"),
        ("Subsystem", "Сервис"),  # внизу панели разделов
    ]
    children += [("StyleItem", name) for name, _, _ in style_defs]
    children += [
        ("Role", "ПолныеПрава"),
        ("CommonForm", "НачальнаяСтраница"),
        ("CommonModule", "КонструкторВидов"),
        ("CommonModule", "Согласование"),
        ("CommonModule", "ДинамическиеФормы"),
        ("CommonModule", "ПечатьДокументов"),
        ("CommonModule", "Уведомления"),
        ("CommonModule", "ТестовыеДанные"),
        ("CommonModule", "Консультант"),
        ("Constant", "АдресSMTP"),
        ("Constant", "ПортSMTP"),
        ("Constant", "ИспользоватьSSL"),
        ("Constant", "ЛогинSMTP"),
        ("Constant", "ПарольSMTP"),
        ("Constant", "АдресОтправителя"),
        ("Constant", "ТаймаутSMTP"),
        ("Constant", "КлючAPIИИ"),
        ("Catalog", "Сотрудники"),
        ("Catalog", "ВидыДокументов"),
        ("Catalog", "ЗначенияПолей"),
        ("Document", "ДокументСЭД"),
        ("ScheduledJob", "ПовторнаяОтправкаУведомлений"),
        ("InformationRegister", "ИсторияСогласования"),
        ("InformationRegister", "ЖурналУведомлений"),
        ("Enum", "КатегорииДокументов"),
        ("Enum", "ТипыПолей"),
        ("Enum", "СтатусыДокументов"),
        ("Enum", "СтатусыНастройкиВида"),
        ("Enum", "РешенияСогласования"),
        ("Enum", "КаналыУведомлений"),
        ("DataProcessor", "ЗагрузкаДемоДанных"),
        ("DataProcessor", "НастройкиПочты"),
        ("DataProcessor", "ПроверкиP0"),
    ]
    writer.raw(
        "Configuration.xml",
        configuration_xml(
            name,
            "ДокМаршрут",
            "Конструктор видов документов и маршрутов согласования (P0).",
            children,
            home_page_work_area="""<HomePageWorkArea>
<WorkingAreaTemplate>TwoColumnsVariableWidth</WorkingAreaTemplate>
<LeftColumn>
<Item>
<Form>CommonForm.НачальнаяСтраница</Form>
<Height>10</Height>
<Visibility>
<xr:Common>true</xr:Common>
</Visibility>
</Item>
</LeftColumn>
</HomePageWorkArea>""",
        ),
    )
    writer.xml("Languages/Русский.xml", language_xml())
    for style_name, style_syn, style_hex in style_defs:
        writer.raw(f"StyleItems/{style_name}.xml", style_item_xml(style_name, style_syn, style_hex))
    writer.xml("Roles/ПолныеПрава.xml", role_xml())
    writer.raw("Roles/ПолныеПрава/Ext/Rights.xml", rights_xml(name))

    # Разделы с StdPicture — иначе на узкой панели только обрезанный текст («Доку», «Вид»).
    # В «Сервис» только обработки (группа команд), без смешения со справочниками/регистрами.
    writer.xml(
        "Subsystems/Документы.xml",
        subsystem_xml(
            "Документы",
            "Документы",
            ["Document.ДокументСЭД"],
            use_one_command=True,
            picture="Document",
        ),
    )
    writer.xml(
        "Subsystems/Конструктор.xml",
        subsystem_xml(
            "Конструктор",
            "Виды документов",
            ["Catalog.ВидыДокументов"],
            use_one_command=True,
            picture="Catalog",
        ),
    )
    writer.xml(
        "Subsystems/Сотрудники.xml",
        subsystem_xml(
            "Сотрудники",
            "Сотрудники",
            ["Catalog.Сотрудники"],
            use_one_command=True,
            picture="User",
        ),
    )
    writer.xml(
        "Subsystems/Уведомления.xml",
        subsystem_xml(
            "Уведомления",
            "Уведомления",
            ["InformationRegister.ЖурналУведомлений"],
            use_one_command=True,
            picture="Message",
        ),
    )
    writer.xml(
        "Subsystems/Сервис.xml",
        subsystem_xml(
            "Сервис",
            "Сервис",
            [
                "DataProcessor.ЗагрузкаДемоДанных",
                "DataProcessor.ПроверкиP0",
                "DataProcessor.НастройкиПочты",
            ],
            use_one_command=False,
            picture="Setting",
        ),
    )

    modules = [
        ("КонструкторВидов", "Конструктор видов", "КонструкторВидов.bsl"),
        ("Согласование", "Согласование документов", "Согласование.bsl"),
        ("ДинамическиеФормы", "Динамические формы", "ДинамическиеФормы.bsl"),
        ("ПечатьДокументов", "Печать документов", "ПечатьДокументов.bsl"),
        ("Уведомления", "Уведомления по SMTP", "Уведомления.bsl"),
        ("ТестовыеДанные", "Тестовые данные", "ТестовыеДанные.bsl"),
        ("Консультант", "Консультант", "Консультант.bsl"),
    ]
    for module_name, module_synonym, bsl_name in modules:
        save_module(
            writer,
            module_xml(module_name, module_synonym),
            f"CommonModules/{module_name}.xml",
            f"CommonModules/{module_name}/Ext/Module.bsl",
            bsl_name,
        )

    writer.xml("Constants/АдресSMTP.xml", constant_xml("АдресSMTP", "Адрес SMTP", type_string(100)))
    writer.xml("Constants/ПортSMTP.xml", constant_xml("ПортSMTP", "Порт SMTP", type_number(5, 0, "Nonnegative")))
    writer.xml("Constants/ИспользоватьSSL.xml", constant_xml("ИспользоватьSSL", "Использовать SSL", type_bool()))
    writer.xml("Constants/ЛогинSMTP.xml", constant_xml("ЛогинSMTP", "Логин SMTP", type_string(100)))
    writer.xml("Constants/ПарольSMTP.xml", constant_xml("ПарольSMTP", "Пароль SMTP", type_string(100), password=True))
    writer.xml("Constants/АдресОтправителя.xml", constant_xml("АдресОтправителя", "Адрес отправителя", type_string(150)))
    writer.xml(
        "Constants/ТаймаутSMTP.xml",
        constant_xml("ТаймаутSMTP", "Таймаут SMTP, сек", type_number(5, 0, "Nonnegative")),
    )
    writer.xml("Constants/КлючAPIИИ.xml", constant_xml("КлючAPIИИ", "Ключ API ИИ", type_string(500), password=True))

    enums = {
        "КатегорииДокументов": ("Категории документов", [("Входящий", "Входящий"), ("Исходящий", "Исходящий"), ("Договорной", "Договорной")]),
        "ТипыПолей": ("Типы полей", [("Строка", "Строка"), ("Число", "Число"), ("Дата", "Дата"), ("ВыборИзСписка", "Выбор из списка")]),
        "СтатусыДокументов": (
            "Статусы документов",
            [
                ("Черновик", "Черновик"),
                ("НаСогласовании", "На согласовании"),
                ("Согласован", "Согласован"),
                ("Отклонен", "Отклонён"),
                ("НаДоработке", "На доработке"),
            ],
        ),
        "СтатусыНастройкиВида": ("Статусы настройки вида", [("Черновик", "Черновик"), ("Готов", "Готов")]),
        "РешенияСогласования": (
            "Решения согласования",
            [
                ("Согласовано", "Согласовано"),
                ("Отклонено", "Отклонено"),
                ("ОтправленНаСогласование", "Отправлен на согласование"),
                ("ВозвращенНаДоработку", "Возвращён на доработку"),
            ],
        ),
        "КаналыУведомлений": (
            "Каналы уведомлений",
            [
                ("ЭлектроннаяПочта", "Электронная почта"),
                ("СистемаВзаимодействия", "Система взаимодействия"),
            ],
        ),
    }
    for enum_name, (synonym, values) in enums.items():
        writer.xml(f"Enums/{enum_name}.xml", enum_xml(enum_name, synonym, values))

    writer.xml(
        "Catalogs/Сотрудники.xml",
        catalog_xml(
            "Сотрудники",
            "Сотрудники",
            150,
            [
                attribute_xml("Должность", "Должность", type_string(100), "Сотрудники.Должность"),
                attribute_xml("Email", "Email", type_string(150), "Сотрудники.Email"),
                attribute_xml(
                    "Руководитель",
                    "Руководитель",
                    type_ref("CatalogRef.Сотрудники"),
                    "Сотрудники.Руководитель",
                    quick_choice=True,
                ),
                attribute_xml("ИмяПользователяИБ", "Пользователь 1С", type_string(100), "Сотрудники.ИБ"),
            ],
            ["ФормаЭлемента", "ФормаСписка"],
            object_form="ФормаЭлемента",
            list_form="ФормаСписка",
            quick_choice=True,
            list_presentation="Список сотрудников",
            description_synonym="ФИО",
        ),
    )

    vid_cols_pоля = [
        column_xml("Порядок", "Порядок", type_number(5, 0, "Nonnegative"), "Виды.Поля.Порядок"),
        column_xml("Заголовок", "Заголовок", type_string(100), "Виды.Поля.Заголовок"),
        column_xml("Идентификатор", "Идентификатор", type_string(50), "Виды.Поля.Идентификатор"),
        column_xml("ТипПоля", "Тип поля", type_enum("ТипыПолей"), "Виды.Поля.ТипПоля"),
        column_xml("Обязательное", "Обязательное", type_bool(), "Виды.Поля.Обязательное"),
        column_xml("Длина", "Длина", type_number(5, 0, "Nonnegative"), "Виды.Поля.Длина"),
        column_xml("Точность", "Точность", type_number(2, 0, "Nonnegative"), "Виды.Поля.Точность"),
        column_xml("Подсказка", "Подсказка", type_string(200), "Виды.Поля.Подсказка"),
        column_xml("Скрыто", "Скрыто", type_bool(), "Виды.Поля.Скрыто"),
    ]
    vid_cols_marshrut = [
        column_xml("НомерЭтапа", "Номер этапа", type_number(3, 0, "Nonnegative"), "Виды.Маршрут.Номер"),
        column_xml("НазваниеЭтапа", "Название этапа", type_string(100), "Виды.Маршрут.Название"),
        column_xml(
            "Согласующий",
            "Согласующий",
            type_ref("CatalogRef.Сотрудники"),
            "Виды.Маршрут.Согласующий",
            quick_choice=True,
        ),
    ]
    vid_attrs = [
        attribute_xml("Категория", "Категория", type_enum("КатегорииДокументов"), "Виды.Категория"),
        attribute_xml("Префикс", "Префикс", type_string(5), "Виды.Префикс"),
        attribute_xml("СтатусНастройки", "Статус настройки", type_enum("СтатусыНастройкиВида"), "Виды.Статус"),
        attribute_xml("Описание", "Описание", type_string(0), "Виды.Описание"),
        tabular_section("Catalog", "ВидыДокументов", "Поля", "Поля вида", vid_cols_pоля),
        tabular_section("Catalog", "ВидыДокументов", "Маршрут", "Маршрут согласования", vid_cols_marshrut),
    ]
    writer.xml(
        "Catalogs/ВидыДокументов.xml",
        catalog_xml(
            "ВидыДокументов",
            "Виды документов",
            150,
            vid_attrs,
            ["ФормаЭлемента", "ФормаМастер", "ФормаСписка"],
            object_form="ФормаЭлемента",
            list_form="ФормаСписка",
            quick_choice=True,
            list_presentation="Список видов",
        ),
    )

    writer.xml(
        "Catalogs/ЗначенияПолей.xml",
        catalog_xml(
            "ЗначенияПолей",
            "Значения полей (справочник выбора)",
            100,
            [attribute_xml("ИдентификаторПоля", "Идентификатор поля", type_string(50), "ЗначенияПолей.ИдПоля")],
            [],
            owners=["Catalog.ВидыДокументов"],
            code_series="WithinOwnerSubordination",
            quick_choice=True,
        ),
    )

    doc_attrs = [
        attribute_xml(
            "ВидДокумента",
            "Вид документа",
            type_ref("CatalogRef.ВидыДокументов"),
            "СЭД.Вид",
            quick_choice=True,
        ),
        attribute_xml("Категория", "Категория", type_enum("КатегорииДокументов"), "СЭД.Категория"),
        attribute_xml("Автор", "Автор", type_ref("CatalogRef.Сотрудники"), "СЭД.Автор", quick_choice=True),
        attribute_xml(
            "Ответственный",
            "Ответственный",
            type_ref("CatalogRef.Сотрудники"),
            "СЭД.Ответственный",
            quick_choice=True,
        ),
        attribute_xml(
            "Руководитель",
            "Руководитель",
            type_ref("CatalogRef.Сотрудники"),
            "СЭД.Руководитель",
            quick_choice=True,
        ),
        attribute_xml("Статус", "Статус", type_enum("СтатусыДокументов"), "СЭД.Статус"),
        attribute_xml("ТекущийЭтап", "Текущий этап", type_number(3, 0, "Nonnegative"), "СЭД.ТекущийЭтап"),
        attribute_xml("ВсегоЭтапов", "Всего этапов", type_number(3, 0, "Nonnegative"), "СЭД.ВсегоЭтапов"),
        attribute_xml("ЦиклСогласования", "Цикл согласования", type_number(3, 0, "Nonnegative"), "СЭД.Цикл"),
        attribute_xml("ТекущийСогласующий", "Текущий согласующий", type_ref("CatalogRef.Сотрудники"), "СЭД.Согласующий"),
        attribute_xml("Содержание", "Суть", type_string(0), "СЭД.Содержание"),
    ]
    ts_values = [
        column_xml("Идентификатор", "Идентификатор", type_string(50), "СЭД.Значения.Ид"),
        column_xml("Заголовок", "Заголовок", type_string(100), "СЭД.Значения.Заголовок"),
        column_xml("ЗначениеСтрока", "Значение", type_string(0), "СЭД.Значения.Значение"),
    ]
    ts_route = [
        column_xml("НомерЭтапа", "Номер этапа", type_number(3, 0, "Nonnegative"), "СЭД.Маршрут.Номер"),
        column_xml("НазваниеЭтапа", "Название этапа", type_string(100), "СЭД.Маршрут.Название"),
        column_xml(
            "Согласующий",
            "Согласующий",
            type_ref("CatalogRef.Сотрудники"),
            "СЭД.Маршрут.Согласующий",
            quick_choice=True,
        ),
    ]
    tabular = (
        tabular_section("Document", "ДокументСЭД", "ЗначенияПолей", "Значения полей", ts_values)
        + tabular_section("Document", "ДокументСЭД", "МаршрутСнимок", "Маршрут согласования", ts_route)
    )
    writer.xml(
        "Documents/ДокументСЭД.xml",
        document_xml_no_posting(
            "ДокументСЭД",
            "Документы",
            doc_attrs,
            tabular,
            ["ФормаДокумента", "ФормаСписка"],
            ["ПечатнаяФормаДокумента"],
            "ФормаДокумента",
        ),
    )
    writer.xml(
        "Documents/ДокументСЭД/Templates/ПечатнаяФормаДокумента.xml",
        template_meta("ПечатнаяФормаДокумента", "Печатная форма документа"),
    )
    writer.raw(
        "Documents/ДокументСЭД/Templates/ПечатнаяФормаДокумента/Ext/Template.xml",
        sed_print_template(),
    )
    writer.xml(
        "ScheduledJobs/ПовторнаяОтправкаУведомлений.xml",
        f"""<ScheduledJob uuid="{uid('job:ПовторнаяОтправкаУведомлений')}">
<Properties>
<Name>ПовторнаяОтправкаУведомлений</Name>
{syn("Повторная отправка уведомлений")}
<Comment/>
<MethodName>CommonModule.Уведомления.ОбработатьОчередьПовторов</MethodName>
<Description>Повторная отправка писем ДокМаршрута</Description>
<Key/>
<Use>false</Use>
<Predefined>true</Predefined>
<RestartCountOnFailure>0</RestartCountOnFailure>
<RestartIntervalOnFailure>0</RestartIntervalOnFailure>
</Properties>
</ScheduledJob>""",
    )
    writer.bsl(
        "Documents/ДокументСЭД/Ext/ObjectModule.bsl",
        read_bsl("ObjectModule_ДокументСЭД.bsl"),
    )
    writer.bsl(
        "Catalogs/ВидыДокументов/Ext/ObjectModule.bsl",
        read_bsl("ObjectModule_ВидыДокументов.bsl"),
    )

    hist_dims = [
        ir_dimension("Документ", "Документ", type_ref("DocumentRef.ДокументСЭД"), "История.Документ"),
        ir_dimension("Цикл", "Цикл", type_number(3, 0, "Nonnegative"), "История.Цикл"),
        ir_dimension("НомерЗаписи", "Номер записи", type_number(6, 0, "Nonnegative"), "История.Номер"),
    ]
    hist_res = [
        ir_resource("Этап", "Этап", type_number(3, 0, "Nonnegative"), "История.Этап"),
        ir_resource("Сотрудник", "Сотрудник", type_ref("CatalogRef.Сотрудники"), "История.Сотрудник"),
        ir_resource("Решение", "Решение", type_enum("РешенияСогласования"), "История.Решение"),
        ir_resource("ДатаВремя", "Дата и время", type_date("DateTime"), "История.ДатаВремя"),
        ir_resource("Комментарий", "Комментарий", type_string(0), "История.Комментарий"),
    ]
    writer.xml(
        "InformationRegisters/ИсторияСогласования.xml",
        information_register_xml("ИсторияСогласования", "История согласования", hist_dims, hist_res),
    )

    journal_dims = [
        ir_dimension("Документ", "Документ", type_ref("DocumentRef.ДокументСЭД"), "Журнал.Документ"),
        ir_dimension("ДатаВремя", "Дата и время", type_date("DateTime"), "Журнал.ДатаВремя"),
        ir_dimension("Получатель", "Получатель", type_string(150), "Журнал.Получатель", deny=False),
        ir_dimension("Канал", "Канал", type_enum("КаналыУведомлений"), "Журнал.Канал"),
        ir_dimension("ИдентификаторПопытки", "Идентификатор попытки", type_string(36), "Журнал.ИдПопытки", deny=False),
    ]
    journal_res = [
        ir_resource("Событие", "Событие", type_string(100), "Журнал.Событие"),
        ir_resource("Успешно", "Успешно", type_bool(), "Журнал.Успешно"),
        ir_resource("ТекстОшибки", "Текст ошибки", type_string(0), "Журнал.ТекстОшибки"),
        ir_resource("Попытка", "Попытка", type_number(3, 0, "Nonnegative"), "Журнал.Попытка"),
        ir_resource("ДанныеПовтора", "Данные для повторной отправки", "<Type><v8:Type>v8:ValueStorage</v8:Type></Type>", "Журнал.Повтор"),
        ir_resource("ПовторитьПосле", "Следующая попытка", type_date("DateTime"), "Журнал.ПовторитьПосле"),
        ir_resource("ВОтправке", "Повторная отправка выполняется", type_bool(), "Журнал.ВОтправке"),
    ]
    writer.xml(
        "InformationRegisters/ЖурналУведомлений.xml",
        information_register_xml(
            "ЖурналУведомлений",
            "Журнал уведомлений",
            journal_dims,
            journal_res,
            list_form="ФормаСписка",
        ),
    )
    save_form(
        writer,
        "InformationRegisters",
        "ЖурналУведомлений",
        "ФормаСписка",
        "Журнал уведомлений",
        journal_list_form_xml(),
        "Form_ЖурналУведомлений_Список.bsl",
    )

    vid_form = FormBuilder()
    vid_form.attr_object("CatalogObject.ВидыДокументов")
    vid_form.attr("БейджСтатуса", "Статус настройки", type_string(40))
    vid_form.command(
        "ПоказатьИнструкцию",
        "Справка",
        "КнопкаИнструкция",
        picture="Information",
        representation="Picture",
        tooltip="Справка: настроить вид документа",
    )
    vid_form.command("ПроверитьШаблон", "Проверить и сохранить шаблон", "КнопкаПроверить", default=True)
    vid_form.command("ОпубликоватьВид", "Опубликовать вид", "КнопкаОпубликовать")
    vid_form.command("ПредпросмотрФормы", "Предпросмотр формы", "КнопкаПредпросмотр")
    vid_form.command("ОткрытьМастер", "Продолжить в мастере", "КнопкаМастер")
    vid_form.command(
        "ЗначенияСписка",
        "Значения списка",
        "КнопкаЗначенияСписка",
        tooltip="Открыть значения выбора для выделенного поля типа «Выбор из списка»",
    )
    vid_form.event("OnCreateAtServer", "ПриСозданииНаСервере")
    vid_form.event("OnReadAtServer", "ПриЧтенииНаСервере")
    vid_form.event("BeforeWriteAtServer", "ПередЗаписьюНаСервере")
    vid_form.event("AfterWriteAtServer", "ПослеЗаписиНаСервере")
    vid_form.event("AfterWrite", "ПослеЗаписи")
    vid_form.decoration(
        "ПодсказкаБрендбук",
        "Черновик нельзя выбрать в документах. Добавьте минимум 1 поле и 2 этапа. Для поля «Выбор из списка» нажмите «Значения списка» и добавьте не меньше двух значений, затем «Проверить и сохранить шаблон» и «Опубликовать вид».",
    )
    vid_form.input("Наименование", "Объект.Description")
    vid_form.begin_group("ГруппаОсновное", "Основное", horizontal=True, representation="NormalSeparation")
    vid_form.input("Категория", "Объект.Категория", back_color="СтатусНаСогласованииФон")
    vid_form.input("Префикс", "Объект.Префикс")
    vid_form.label_field("БейджСтатуса", "БейджСтатуса", title_location="None")
    vid_form.end_group()
    vid_form.input("Описание", "Объект.Описание", multiline=True)
    vid_form.begin_group("ГруппаПоля", "1. Поля документа", representation="NormalSeparation")
    vid_form.table(
        "Поля",
        "Объект.Поля",
        [
            ("Порядок", "Объект.Поля.Порядок"),
            ("Заголовок", "Объект.Поля.Заголовок"),
            ("Идентификатор", "Объект.Поля.Идентификатор"),
            ("ТипПоля", "Объект.Поля.ТипПоля"),
            ("Обязательное", "Объект.Поля.Обязательное"),
        ],
        on_start_edit="ПоляПриНачалеРедактирования",
    )
    vid_form.end_group()
    vid_form.begin_group("ГруппаМаршрут", "2. Маршрут согласования", representation="NormalSeparation")
    vid_form.table(
        "Маршрут",
        "Объект.Маршрут",
        [
            ("НомерЭтапа", "Объект.Маршрут.НомерЭтапа"),
            ("НазваниеЭтапа", "Объект.Маршрут.НазваниеЭтапа"),
            ("Согласующий", "Объект.Маршрут.Согласующий"),
        ],
    )
    vid_form.end_group()
    save_form(
        writer,
        "Catalogs",
        "ВидыДокументов",
        "ФормаЭлемента",
        "Форма элемента вида",
        vid_form.xml(),
        "Form_ВидыДокументов.bsl",
    )

    vid_list = FormBuilder()
    # Список видов: наименование + метаданные шаблона.
    save_form(
        writer,
        "Catalogs",
        "ВидыДокументов",
        "ФормаСписка",
        "Виды документов",
        kinds_list_form_xml(),
        "Form_ВидыДокументов_Список.bsl",
    )

    # Карточка: шапка (вид+категория+статус) → поля | кто → суть → маршрут/история.
    doc_form = FormBuilder()
    doc_form.attr_object("DocumentObject.ДокументСЭД")
    doc_form.attr("БейджСтатуса", "Статус", type_string(60))
    doc_form.attr("ПодписьСогласующего", "Сейчас согласует", type_string(150))
    doc_form.attr("ПодсказкаШага", "Подсказка", type_string(200))
    doc_form.attr("ПодписьПолучателейПисем", "Получатели писем", type_string(0))
    doc_form.attr("ПредыдущийВид", "Предыдущий вид", type_ref("CatalogRef.ВидыДокументов"))
    doc_form.attr("ПредыдущаяКатегория", "Предыдущая категория", type_enum("КатегорииДокументов"))
    doc_form.attr("РежимПредпросмотра", "Режим предпросмотра", type_bool())
    doc_form.attr_table(
        "ПоляФормы",
        "Поля формы",
        [
            ("Имя", "Имя", type_string(80)),
            ("Идентификатор", "Идентификатор", type_string(50)),
            ("Заголовок", "Заголовок", type_string(150)),
            ("Обязательное", "Обязательное", type_bool()),
            ("Изменено", "Изменено", type_bool()),
            ("ТипПоля", "Тип поля", type_enum("ТипыПолей")),
        ],
    )
    doc_form.parameter("ВидДляПредпросмотра", type_ref("CatalogRef.ВидыДокументов"))
    doc_form.attr_table(
        "Таймлайн",
        "Маршрут согласования",
        [
            ("Номер", "№", type_number(3, 0, "Nonnegative")),
            ("Название", "Этап", type_string(100)),
            ("Согласующий", "Согласующий", type_string(150)),
            ("Состояние", "Состояние", type_string(20)),
        ],
    )
    doc_form.attr_table(
        "История",
        "История согласования",
        [
            ("ДатаВремя", "Дата", type_date("DateTime")),
            ("Этап", "Этап", type_number(3, 0, "Nonnegative")),
            ("Сотрудник", "Сотрудник", type_string(150)),
            ("Решение", "Решение", type_string(80)),
            ("Комментарий", "Комментарий", type_string(0)),
        ],
    )
    doc_form.command(
        "ПоказатьИнструкцию",
        "Справка",
        "КнопкаИнструкция",
        picture="Information",
        representation="Picture",
        tooltip="Справка: создать документ и отправить на согласование",
    )
    doc_form.command("ОтправитьНаСогласование", "Отправить на согласование", "КнопкаОтправить")

    doc_form.command("Согласовать", "Согласовать", "КнопкаСогласовать")
    doc_form.command("Отклонить", "Отклонить", "КнопкаОтклонить")
    doc_form.command("ВернутьНаДоработку", "Вернуть на доработку", "КнопкаДоработка")
    doc_form.command("ПечатьPDF", "Предпросмотр", "КнопкаПечать")
    doc_form.command("ОтправитьПечатнуюФорму", "Отправить на почту", "КнопкаОтправитьФорму")
    doc_form.command(
        "СоздатьНовыйВид",
        "Новый вид",
        tooltip="Открыть мастер создания вида документа",
        add_to_bar=False,
    )
    doc_form.event("OnCreateAtServer", "ПриСозданииНаСервере")
    doc_form.event("OnReadAtServer", "ПриЧтенииНаСервере")
    doc_form.event("AfterWriteAtServer", "ПослеЗаписиНаСервере")
    doc_form.event("BeforeWrite", "ПередЗаписью")
    doc_form.event("BeforeWriteAtServer", "ПередЗаписьюНаСервере")
    doc_form.event("NotificationProcessing", "ОбработкаОповещения")

    doc_form.begin_group("ГруппаШапка", "", horizontal=True, representation="None", show_title=False)
    doc_form.input("Категория", "Объект.Категория", on_change="КатегорияПриИзменении")
    doc_form.begin_group(
        "ГруппаВидДокумента",
        "",
        horizontal=True,
        representation="None",
        show_title=False,
    )
    doc_form.input(
        "ВидДокумента",
        "Объект.ВидДокумента",
        on_change="ВидДокументаПриИзменении",
    )
    doc_form.usual_button("КнопкаНовыйВид", "СоздатьНовыйВид")
    doc_form.end_group()
    doc_form.label_field("БейджСтатуса", "БейджСтатуса", title_location="Top", width=18)
    doc_form.label_field("ПодписьСогласующего", "ПодписьСогласующего", title_location="Top")
    doc_form.end_group()

    doc_form.begin_group("ГруппаНомерДата", "", horizontal=True, representation="None", show_title=False)
    doc_form.input("Номер", "Объект.Номер")
    doc_form.input("Дата", "Объект.Дата")
    doc_form.end_group()

    doc_form.label_field(
        "ПодсказкаШага",
        "ПодсказкаШага",
        title_location="None",
        height=2,
        horizontal_stretch=True,
    )

    doc_form.begin_group("ГруппаКолонки", "", horizontal=True, representation="None", show_title=False)
    doc_form.begin_group("ГруппаПоля", "Поля документа", representation="NormalSeparation")
    doc_form.begin_group("ПоляВида", "", show_title=False, representation="None")
    doc_form.end_group()
    doc_form.table(
        "ЗначенияПолей",
        "Объект.ЗначенияПолей",
        [
            ("Заголовок", "Объект.ЗначенияПолей.Заголовок", True),
            ("ЗначениеСтрока", "Объект.ЗначенияПолей.ЗначениеСтрока", False),
        ],
        visible=False,
    )
    doc_form.end_group()
    doc_form.begin_group("ГруппаУчастники", "Кто участвует", representation="NormalSeparation")
    doc_form.input("Автор", "Объект.Автор")
    doc_form.input("Ответственный", "Объект.Ответственный", on_change="УчастникПриИзменении")
    doc_form.input("Руководитель", "Объект.Руководитель", on_change="УчастникПриИзменении")
    doc_form.end_group()
    doc_form.end_group()

    doc_form.label_field(
        "ПодписьПолучателейПисем",
        "ПодписьПолучателейПисем",
        title_location="None",
        height=2,
        horizontal_stretch=True,
    )
    doc_form.input("Содержание", "Объект.Содержание", multiline=True, height=3)

    doc_form.begin_group(
        "ГруппаМаршрут",
        "Маршрут согласования",
        representation="NormalSeparation",
        collapsible=True,
        collapsed=True,
    )
    doc_form.form_table(
        "Таймлайн",
        "Таймлайн",
        [
            ("Номер", "Таймлайн.Номер"),
            ("Название", "Таймлайн.Название"),
            ("Согласующий", "Таймлайн.Согласующий"),
            ("Состояние", "Таймлайн.Состояние"),
        ],
    )
    doc_form.end_group()

    doc_form.begin_group(
        "ГруппаИстория",
        "История согласования",
        representation="NormalSeparation",
        collapsible=True,
        collapsed=True,
    )
    doc_form.form_table(
        "История",
        "История",
        [
            ("ДатаВремя", "История.ДатаВремя"),
            ("Этап", "История.Этап"),
            ("Сотрудник", "История.Сотрудник"),
            ("Решение", "История.Решение"),
            ("Комментарий", "История.Комментарий"),
        ],
    )
    doc_form.end_group()
    save_form(
        writer,
        "Documents",
        "ДокументСЭД",
        "ФормаДокумента",
        "Форма документа",
        doc_form.xml(),
        "Form_ДокументСЭД.bsl",
    )

    # Сотрудники — форма с подсказкой про привязку к пользователю ИБ.
    staff_form = FormBuilder()
    staff_form.attr_object("CatalogObject.Сотрудники")
    staff_form.command(
        "ПоказатьИнструкцию",
        "Справка",
        "КнопкаИнструкция",
        picture="Information",
        representation="Picture",
        tooltip="Справка: карточка сотрудника",
    )
    staff_form.decoration(
        "ПодсказкаИБ",
        "В поле «Пользователь 1С» укажите имя пользователя информационной базы. Без него не работают «Мои задачи» и проверка текущего согласующего.",
    )
    staff_form.input("Наименование", "Объект.Description")
    staff_form.input("Должность", "Объект.Должность")
    staff_form.input("Email", "Объект.Email")
    staff_form.input("Руководитель", "Объект.Руководитель")
    staff_form.input("ИмяПользователяИБ", "Объект.ИмяПользователяИБ")
    save_form(
        writer,
        "Catalogs",
        "Сотрудники",
        "ФормаЭлемента",
        "Форма элемента",
        staff_form.xml(),
        "Form_Сотрудники.bsl",
    )
    save_form(
        writer,
        "Catalogs",
        "Сотрудники",
        "ФормаСписка",
        "Сотрудники",
        catalog_list_form_xml(
            "Catalog.Сотрудники",
            [
                ("Наименование", "Список.Description"),
                ("Должность", "Список.Должность"),
                ("Email", "Список.Email"),
                ("ИмяПользователяИБ", "Список.ИмяПользователяИБ"),
            ],
            yellow_create=True,
        ),
        "Form_Сотрудники_Список.bsl",
    )
    save_form(
        writer,
        "Documents",
        "ДокументСЭД",
        "ФормаСписка",
        "Документы",
        document_list_form_xml(),
        "Form_ДокументСЭД_Список.bsl",
    )

    writer.xml("DataProcessors/ЗагрузкаДемоДанных.xml", processor_xml("ЗагрузкаДемоДанных", "Загрузка демо-данных", "Форма"))
    writer.xml("DataProcessors/НастройкиПочты.xml", processor_xml("НастройкиПочты", "Настройки почты", "Форма"))
    writer.xml("DataProcessors/ПроверкиP0.xml", processor_xml("ПроверкиP0", "Проверки P0", "Форма"))

    demo = FormBuilder()
    demo.attr_object("DataProcessorObject.ЗагрузкаДемоДанных")
    demo.attr("РезультатЗагрузки", "Результат", type_string(0))
    demo.command("СоздатьДемоБазу", "Загрузить демо-данные", "КнопкаДемо")
    demo.decoration(
        "Пояснение",
        "Добавляет 5 сотрудников, 3 вида документов и 6 документов СЭД. Повторный запуск создаёт только то, чего ещё нет.",
    )
    demo.input("РезультатЗагрузки", "РезультатЗагрузки", readonly=True, multiline=True)
    save_form(writer, "DataProcessors", "ЗагрузкаДемоДанных", "Форма", "Форма", demo.xml(), "Form_Демо.bsl")

    mail = FormBuilder()
    mail.attr_object("DataProcessorObject.НастройкиПочты")
    mail.attr("АдресSMTP", "Адрес SMTP", type_string(100))
    mail.attr("ПортSMTP", "Порт SMTP", type_number(5, 0, "Nonnegative"))
    mail.attr("ЛогинSMTP", "Логин SMTP", type_string(100))
    mail.attr("ПарольSMTP", "Пароль SMTP", type_string(100))
    mail.attr("АдресОтправителя", "Адрес отправителя", type_string(150))
    mail.attr("ТаймаутSMTP", "Таймаут, сек", type_number(5, 0, "Nonnegative"))
    mail.attr("ИспользоватьSSL", "Использовать SSL", type_bool())
    mail.attr("Автоповтор", "Автоматически повторять неудачные отправки", type_bool())
    mail.attr("ПодписьПароля", "Подсказка пароля", type_string(0))
    mail.attr("ПарольПоказан", "Пароль показан", type_bool())
    mail.command(
        "ПоказатьИнструкцию",
        "Справка",
        "КнопкаИнструкция",
        picture="Information",
        representation="Picture",
        tooltip="Справка: настройка SMTP",
    )
    mail.command("ЗаписатьНастройки", "Записать настройки", "КнопкаЗаписать", default=True)
    mail.command("ПроверитьОтправку", "Проверить отправку", "КнопкаПроверить")
    mail.command(
        "ПоказатьПароль",
        "Показать пароль",
        "КнопкаПоказатьПароль",
        picture="ShowData",
        representation="Picture",
        tooltip="Показать или скрыть пароль",
        add_to_bar=False,
    )
    mail.event("OnCreateAtServer", "ПриСозданииНаСервере")
    mail.begin_group("ГруппаСервер", "Сервер", representation="NormalSeparation")
    mail.input("АдресSMTP", "АдресSMTP")
    mail.input("ПортSMTP", "ПортSMTP")
    mail.check("ИспользоватьSSL", "ИспользоватьSSL")
    mail.input("ТаймаутSMTP", "ТаймаутSMTP")
    mail.end_group()
    mail.begin_group("ГруппаУчётнаяЗапись", "Учётная запись", representation="NormalSeparation")
    mail.input("ЛогинSMTP", "ЛогинSMTP")
    mail.begin_group(
        "ГруппаПароль",
        "",
        horizontal=True,
        representation="None",
        show_title=False,
    )
    mail.input("ПарольSMTP", "ПарольSMTP", password=True)
    mail.usual_button(
        "КнопкаПоказатьПароль",
        "ПоказатьПароль",
        representation="Picture",
        picture="ShowData",
    )
    mail.end_group()
    mail.label_field(
        "ПодписьПароля",
        "ПодписьПароля",
        title_location="None",
        height=2,
        horizontal_stretch=True,
    )
    mail.end_group()
    mail.begin_group("ГруппаОтправитель", "Отправитель", representation="NormalSeparation")
    mail.input("АдресОтправителя", "АдресОтправителя")
    mail.check("Автоповтор", "Автоповтор")
    mail.end_group()
    save_form(writer, "DataProcessors", "НастройкиПочты", "Форма", "Форма", mail.xml(), "Form_НастройкиПочты.bsl")

    checks = FormBuilder()
    checks.attr_object("DataProcessorObject.ПроверкиP0")
    checks.attr("ЖурналПроверок", "Журнал", type_string(0))
    checks.command(
        "ПоказатьИнструкцию",
        "Справка",
        "КнопкаИнструкция",
        picture="Information",
        representation="Picture",
        tooltip="Справка: как запустить проверки",
    )
    checks.command("ЗапуститьПроверки", "Запустить проверки", "КнопкаПроверки", default=True)
    checks.input("ЖурналПроверок", "ЖурналПроверок", readonly=True, multiline=True)
    save_form(writer, "DataProcessors", "ПроверкиP0", "Форма", "Форма", checks.xml(), "Form_ПроверкиP0.bsl")

    denis_root = ROOT / "модули_команды" / "denis" / "ДокМаршрут"
    for relative in (
        "Catalogs/ВидыДокументов/Forms/ФормаМастер.xml",
        "Catalogs/ВидыДокументов/Forms/ФормаМастер/Ext/Form.xml",
        "CommonForms/НачальнаяСтраница.xml",
    ):
        writer.raw(relative, (denis_root / relative).read_text(encoding="utf-8"))
    writer.raw(
        "CommonForms/НачальнаяСтраница/Ext/Form.xml",
        (ROOT / "tools" / "forms" / "dokmarshrut" / "НачальнаяСтраница.xml").read_text(
            encoding="utf-8"
        ),
    )
    writer.bsl(
        "Catalogs/ВидыДокументов/Forms/ФормаМастер/Ext/Form/Module.bsl",
        read_bsl("Form_ВидыДокументов_Мастер.bsl"),
    )
    writer.bsl(
        "CommonForms/НачальнаяСтраница/Ext/Form/Module.bsl",
        read_bsl("Form_НачальнаяСтраница.bsl"),
    )
    writer.bsl("Ext/ManagedApplicationModule.bsl", read_bsl("ManagedApplicationModule.bsl"))


def validate(root: Path):
    errors = []
    for path in root.rglob("*.xml"):
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"{path}: {exc}")
    cfg = root / "Configuration.xml"
    if not cfg.exists():
        errors.append("Configuration.xml missing")
    elif "ДокументСЭД" not in cfg.read_text(encoding="utf-8"):
        errors.append("ДокументСЭД not in configuration")
    doc = root / "Documents" / "ДокументСЭД.xml"
    if doc.exists() and "<Posting>Deny</Posting>" not in doc.read_text(encoding="utf-8"):
        errors.append("ДокументСЭД must not post")
    return errors


def main():
    out = ROOT / "src" / "ДокМаршрут"
    build_dokmarshrut(out)
    problems = validate(out)
    if problems:
        print("PROBLEMS")
        print("\n".join(problems))
        return 1
    print("OK", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())