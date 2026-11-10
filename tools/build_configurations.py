# -*- coding: utf-8 -*-
"""Сборка двух выгрузок конфигурации 1С (формат XML 2.17)."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cf_common import (  # noqa: E402
    CLASS_IDS,
    FormBuilder,
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

ROOT = Path(__file__).resolve().parents[1]
BSL = ROOT / "tools" / "bsl"


def read_bsl(relative: str) -> str:
    return (BSL / relative).read_text(encoding="utf-8")


def configuration_xml(name, synonym, comment, children):
    contained = []
    for class_id in CLASS_IDS:
        contained.append(
            "<xr:ContainedObject>"
            f"<xr:ClassId>{class_id}</xr:ClassId>"
            f"<xr:ObjectId>{uid(name + ':' + class_id)}</xr:ObjectId>"
            "</xr:ContainedObject>"
        )
    child_xml = "".join(f"<{kind}>{obj}</{kind}>" for kind, obj in children)
    body = f"""<Configuration uuid="{uid(name)}">
<InternalInfo>{''.join(contained)}</InternalInfo>
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment>{esc(comment)}</Comment>
<NamePrefix/>
<ConfigurationExtensionCompatibilityMode>Version8_3_24</ConfigurationExtensionCompatibilityMode>
<DefaultRunMode>ManagedApplication</DefaultRunMode>
<UsePurposes>
<v8:Value xsi:type="app:ApplicationUsePurpose">PlatformApplication</v8:Value>
</UsePurposes>
<ScriptVariant>Russian</ScriptVariant>
<DefaultRoles>
<xr:Item xsi:type="xr:MDObjectRef">Role.ПолныеПрава</xr:Item>
</DefaultRoles>
<Vendor/>
<Version>1.0.0.1</Version>
<UpdateCatalogAddress/>
<IncludeHelpInContents>false</IncludeHelpInContents>
<UseManagedFormInOrdinaryApplication>false</UseManagedFormInOrdinaryApplication>
<UseOrdinaryFormInManagedApplication>false</UseOrdinaryFormInManagedApplication>
<AdditionalFullTextSearchDictionaries/>
<CommonSettingsStorage/>
<ReportsUserSettingsStorage/>
<ReportsVariantsStorage/>
<FormDataSettingsStorage/>
<DynamicListsUserSettingsStorage/>
<URLExternalDataStorage/>
<Content/>
<DefaultReportForm/>
<DefaultReportVariantForm/>
<DefaultReportSettingsForm/>
<DefaultReportAppearanceTemplate/>
<DefaultDynamicListSettingsForm/>
<DefaultSearchForm/>
<DefaultDataHistoryChangeHistoryForm/>
<DefaultDataHistoryVersionDataForm/>
<DefaultDataHistoryVersionDifferencesForm/>
<DefaultCollaborationSystemUsersChoiceForm/>
<RequiredMobileApplicationPermissions/>
<UsedMobileApplicationFunctionalities/>
<StandaloneConfigurationRestrictionRoles/>
<MobileApplicationURLs/>
<AllowedIncomingShareRequestTypes/>
<MainClientApplicationWindowMode>Normal</MainClientApplicationWindowMode>
<DefaultInterface/>
<DefaultStyle/>
<DefaultLanguage>Language.Русский</DefaultLanguage>
<BriefInformation/>
<DetailedInformation/>
<Copyright/>
<VendorInformationAddress/>
<ConfigurationInformationAddress/>
<DataLockControlMode>Managed</DataLockControlMode>
<ObjectAutonumerationMode>NotAutoFree</ObjectAutonumerationMode>
<ModalityUseMode>DontUse</ModalityUseMode>
<SynchronousPlatformExtensionAndAddInCallUseMode>DontUse</SynchronousPlatformExtensionAndAddInCallUseMode>
<InterfaceCompatibilityMode>Taxi</InterfaceCompatibilityMode>
<DatabaseTablespacesUseMode>DontUse</DatabaseTablespacesUseMode>
<CompatibilityMode>Version8_3_24</CompatibilityMode>
</Properties>
<ChildObjects>
{child_xml}
</ChildObjects>
</Configuration>"""
    return wrap(body)


def language_xml():
    return f"""<Language uuid="{uid('lang:Русский')}">
<Properties>
<Name>Русский</Name>
{syn('Русский')}
<Comment/>
<LanguageCode>ru</LanguageCode>
</Properties>
</Language>"""


def role_xml():
    return f"""<Role uuid="{uid('role:ПолныеПрава')}">
<Properties>
<Name>ПолныеПрава</Name>
{syn('Полные права')}
<Comment/>
</Properties>
</Role>"""


def rights_xml(config_name):
    rights = [
        "Administration",
        "DataAdministration",
        "ThinClient",
        "WebClient",
        "ThickClient",
        "MainWindowModeNormal",
        "MainWindowModeWorkplace",
        "MainWindowModeEmbeddedWorkplace",
        "MainWindowModeFullscreenWorkplace",
        "MainWindowModeKiosk",
        "SaveUserData",
        "Output",
        "TechnicalSpecialistMode",
    ]
    items = "".join(
        f"<right><name>{name}</name><value>true</value></right>" for name in rights
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Rights xmlns="http://v8.1c.ru/8.2/roles" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Rights" version="2.17">
<setForNewObjects>true</setForNewObjects>
<setForAttributesByDefault>true</setForAttributesByDefault>
<independentRightsOfChildObjects>false</independentRightsOfChildObjects>
<object>
<name>Configuration.{config_name}</name>
{items}
</object>
</Rights>
"""


def subsystem_xml(name, synonym, content_refs):
    items = "".join(
        f'<xr:Item xsi:type="xr:MDObjectRef">{ref}</xr:Item>' for ref in content_refs
    )
    return f"""<Subsystem uuid="{uid('subsystem:' + name)}">
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<IncludeHelpInContents>false</IncludeHelpInContents>
<IncludeInCommandInterface>true</IncludeInCommandInterface>
<UseOneCommand>false</UseOneCommand>
<Explanation/>
<Picture/>
<Content>
{items}
</Content>
</Properties>
<ChildObjects/>
</Subsystem>"""


def module_xml(name, synonym):
    return f"""<CommonModule uuid="{uid('module:' + name)}">
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<Global>false</Global>
<ClientManagedApplication>false</ClientManagedApplication>
<Server>true</Server>
<ExternalConnection>false</ExternalConnection>
<ClientOrdinaryApplication>false</ClientOrdinaryApplication>
<ServerCall>true</ServerCall>
<Privileged>false</Privileged>
<ReturnValuesReuse>DontUse</ReturnValuesReuse>
</Properties>
</CommonModule>"""


def constant_xml(name, synonym, type_xml, password=False):
    return f"""<Constant uuid="{uid('const:' + name)}">
<InternalInfo>
{generated([
    (f'ConstantManager.{name}', 'Manager', name + '.manager'),
    (f'ConstantValueManager.{name}', 'ValueManager', name + '.value'),
    (f'ConstantValueKey.{name}', 'ValueKey', name + '.key'),
])}
</InternalInfo>
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
{type_xml}
<UseStandardCommands>true</UseStandardCommands>
<DefaultForm/>
<ExtendedPresentation/>
<Explanation/>
<PasswordMode>{"true" if password else "false"}</PasswordMode>
<Format/>
<EditFormat/>
<ToolTip/>
<MarkNegatives>false</MarkNegatives>
<Mask/>
<MultiLine>false</MultiLine>
<ExtendedEdit>false</ExtendedEdit>
<MinValue xsi:nil="true"/>
<MaxValue xsi:nil="true"/>
<FillChecking>DontCheck</FillChecking>
<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>
<ChoiceParameterLinks/>
<ChoiceParameters/>
<QuickChoice>Auto</QuickChoice>
<ChoiceForm/>
<LinkByType/>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
<DataLockControlMode>Managed</DataLockControlMode>
<DataHistory>DontUse</DataHistory>
</Properties>
</Constant>"""


def catalog_xml(name, synonym, description_length, attributes, forms, owners=None, code_series="WholeCatalog", object_form=""):
    owner_xml = "<Owners/>"
    if owners:
        owner_xml = "<Owners>" + "".join(
            f'<xr:Item xsi:type="xr:MDObjectRef">{item}</xr:Item>' for item in owners
        ) + "</Owners>"
    object_form_xml = f"<DefaultObjectForm>Catalog.{name}.Form.{object_form}</DefaultObjectForm>" if object_form else "<DefaultObjectForm/>"
    input_fields = "".join(
        f"<xr:Field>Catalog.{name}.StandardAttribute.{field}</xr:Field>"
        for field in ("Description", "Code")
    )
    form_refs = "".join(f"<Form>{form_name}</Form>" for form_name in forms)
    internal = generated([
        (f"CatalogObject.{name}", "Object", name + ".obj"),
        (f"CatalogRef.{name}", "Ref", name + ".ref"),
        (f"CatalogSelection.{name}", "Selection", name + ".sel"),
        (f"CatalogList.{name}", "List", name + ".list"),
        (f"CatalogManager.{name}", "Manager", name + ".man"),
    ])
    return f"""<Catalog uuid="{uid('catalog:' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<Hierarchical>false</Hierarchical>
<HierarchyType>HierarchyFoldersAndItems</HierarchyType>
<LimitLevelCount>false</LimitLevelCount>
<LevelCount>2</LevelCount>
<FoldersOnTop>true</FoldersOnTop>
<UseStandardCommands>true</UseStandardCommands>
{owner_xml}
<SubordinationUse>ToItems</SubordinationUse>
<CodeLength>9</CodeLength>
<DescriptionLength>{description_length}</DescriptionLength>
<CodeType>String</CodeType>
<CodeAllowedLength>Variable</CodeAllowedLength>
<CodeSeries>{code_series}</CodeSeries>
<CheckUnique>true</CheckUnique>
<Autonumbering>true</Autonumbering>
<DefaultPresentation>AsDescription</DefaultPresentation>
<Characteristics/>
<PredefinedDataUpdate>Auto</PredefinedDataUpdate>
<EditType>InDialog</EditType>
<QuickChoice>false</QuickChoice>
<ChoiceMode>BothWays</ChoiceMode>
<InputByString>{input_fields}</InputByString>
<SearchStringModeOnInputByString>Begin</SearchStringModeOnInputByString>
<FullTextSearchOnInputByString>DontUse</FullTextSearchOnInputByString>
<ChoiceDataGetModeOnInputByString>Directly</ChoiceDataGetModeOnInputByString>
{object_form_xml}
<DefaultFolderForm/>
<DefaultListForm/>
<DefaultChoiceForm/>
<DefaultFolderChoiceForm/>
<AuxiliaryObjectForm/>
<AuxiliaryFolderForm/>
<AuxiliaryListForm/>
<AuxiliaryChoiceForm/>
<AuxiliaryFolderChoiceForm/>
<IncludeHelpInContents>false</IncludeHelpInContents>
<BasedOn/>
<DataLockFields/>
<DataLockControlMode>Managed</DataLockControlMode>
<FullTextSearch>Use</FullTextSearch>
<ObjectPresentation/>
<ExtendedObjectPresentation/>
<ListPresentation/>
<ExtendedListPresentation/>
<Explanation/>
<CreateOnInput>Use</CreateOnInput>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
<DataHistory>DontUse</DataHistory>
<UpdateDataHistoryImmediatelyAfterWrite>false</UpdateDataHistoryImmediatelyAfterWrite>
<ExecuteAfterWriteDataHistoryVersionProcessing>false</ExecuteAfterWriteDataHistoryVersionProcessing>
</Properties>
<ChildObjects>
{''.join(attributes)}
{form_refs}
</ChildObjects>
</Catalog>"""


def document_xml(name, synonym, attributes, tabular, forms, templates, register_name, object_form):
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
<NumberLength>9</NumberLength>
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
<DefaultListForm/>
<DefaultChoiceForm/>
<AuxiliaryObjectForm/>
<AuxiliaryListForm/>
<AuxiliaryChoiceForm/>
<Posting>Allow</Posting>
<RealTimePosting>Deny</RealTimePosting>
<RegisterRecordsDeletion>AutoDeleteOnUnpost</RegisterRecordsDeletion>
<RegisterRecordsWritingOnPost>WriteSelected</RegisterRecordsWritingOnPost>
<SequenceFilling>AutoFillOff</SequenceFilling>
<RegisterRecords>
<xr:Item xsi:type="xr:MDObjectRef">AccumulationRegister.{register_name}</xr:Item>
</RegisterRecords>
<PostInPrivilegedMode>true</PostInPrivilegedMode>
<UnpostInPrivilegedMode>true</UnpostInPrivilegedMode>
<IncludeHelpInContents>false</IncludeHelpInContents>
<DataLockFields/>
<DataLockControlMode>Managed</DataLockControlMode>
<FullTextSearch>Use</FullTextSearch>
<ObjectPresentation/>
<ExtendedObjectPresentation/>
<ListPresentation/>
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
{tabular}
{template_refs}
</ChildObjects>
</Document>"""


def enum_xml(name, synonym, values):
    internal = generated([
        (f"EnumRef.{name}", "Ref", name + ".ref"),
        (f"EnumManager.{name}", "Manager", name + ".man"),
        (f"EnumList.{name}", "List", name + ".list"),
    ])
    value_xml = []
    for value_name, value_synonym in values:
        value_xml.append(
            f'<EnumValue uuid="{uid(name + "." + value_name)}">'
            "<Properties>"
            f"<Name>{value_name}</Name>"
            f"{syn(value_synonym)}"
            "<Comment/>"
            "</Properties></EnumValue>"
        )
    return f"""<Enum uuid="{uid('enum:' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<UseStandardCommands>true</UseStandardCommands>
<QuickChoice>true</QuickChoice>
<ChoiceMode>BothWays</ChoiceMode>
<DefaultListForm/>
<DefaultChoiceForm/>
<AuxiliaryListForm/>
<AuxiliaryChoiceForm/>
<ListPresentation/>
<ExtendedListPresentation/>
<Explanation/>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
</Properties>
<ChildObjects>
{''.join(value_xml)}
</ChildObjects>
</Enum>"""


def register_xml(name, synonym, register_type, resources, dimensions):
    internal = generated([
        (f"AccumulationRegisterRecord.{name}", "Record", name + ".rec"),
        (f"AccumulationRegisterManager.{name}", "Manager", name + ".man"),
        (f"AccumulationRegisterSelection.{name}", "Selection", name + ".sel"),
        (f"AccumulationRegisterList.{name}", "List", name + ".list"),
        (f"AccumulationRegisterRecordSet.{name}", "RecordSet", name + ".set"),
        (f"AccumulationRegisterRecordKey.{name}", "RecordKey", name + ".key"),
    ])
    return f"""<AccumulationRegister uuid="{uid('reg:' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<UseStandardCommands>true</UseStandardCommands>
<DefaultListForm/>
<AuxiliaryListForm/>
<RegisterType>{register_type}</RegisterType>
<IncludeHelpInContents>false</IncludeHelpInContents>
<DataLockControlMode>Managed</DataLockControlMode>
<FullTextSearch>DontUse</FullTextSearch>
<EnableTotalsSplitting>true</EnableTotalsSplitting>
<ListPresentation/>
<ExtendedListPresentation/>
<Explanation/>
</Properties>
<ChildObjects>
{''.join(resources)}
{''.join(dimensions)}
</ChildObjects>
</AccumulationRegister>"""


def processor_xml(name, synonym, form_name):
    internal = generated([
        (f"DataProcessorObject.{name}", "Object", name + ".obj"),
        (f"DataProcessorManager.{name}", "Manager", name + ".man"),
    ])
    return f"""<DataProcessor uuid="{uid('dp:' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<UseStandardCommands>true</UseStandardCommands>
<DefaultForm>DataProcessor.{name}.Form.{form_name}</DefaultForm>
<AuxiliaryForm/>
<IncludeHelpInContents>false</IncludeHelpInContents>
<ExtendedPresentation/>
<Explanation/>
</Properties>
<ChildObjects>
<Form>{form_name}</Form>
</ChildObjects>
</DataProcessor>"""


def template_meta(name, synonym):
    return f"""<Template uuid="{uid('tpl:' + name)}">
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<TemplateType>SpreadsheetDocument</TemplateType>
</Properties>
</Template>"""


def receipt_template():
    return """<?xml version="1.0" encoding="UTF-8"?>
<document xmlns="http://v8.1c.ru/8.2/data/spreadsheet" xmlns:style="http://v8.1c.ru/8.1/data/ui/style" xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<languageSettings>
<currentLanguage>ru</currentLanguage>
<defaultLanguage>ru</defaultLanguage>
<languageInfo>
<id>ru</id>
<code>Русский</code>
<description>Русский</description>
</languageInfo>
</languageSettings>
<columns>
<size>3</size>
<columnsItem><index>0</index><column><formatIndex>1</formatIndex></column></columnsItem>
<columnsItem><index>1</index><column><formatIndex>2</formatIndex></column></columnsItem>
<columnsItem><index>2</index><column><formatIndex>3</formatIndex></column></columnsItem>
</columns>
<rowsItem><index>0</index><row><formatIndex>4</formatIndex><c><c><f>5</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Поступление товаров на склад № [Номер] от [Дата]</v8:content></v8:item></tl></c></c></row></rowsItem>
<rowsItem><index>1</index><row><c><c><f>6</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Получатель: [АдресЭлектроннойПочты]</v8:content></v8:item></tl></c></c></row></rowsItem>
<rowsItem><index>2</index><row><empty>true</empty></row></rowsItem>
<rowsItem><index>3</index><row>
<c><c><f>7</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>№ п/п</v8:content></v8:item></tl></c></c>
<c><c><f>7</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Товар</v8:content></v8:item></tl></c></c>
<c><c><f>7</f><tl><v8:item><v8:lang>ru</v8:lang><v8:content>Количество, шт.</v8:content></v8:item></tl></c></c>
</row></rowsItem>
<rowsItem><index>4</index><row>
<c><c><f>8</f><parameter>НомерСтроки</parameter></c></c>
<c><c><f>9</f><parameter>Товар</parameter></c></c>
<c><c><f>8</f><parameter>Количество</parameter></c></c>
</row></rowsItem>
<templateMode>true</templateMode>
<defaultFormatIndex>10</defaultFormatIndex>
<height>5</height>
<vgRows>5</vgRows>
<merge><r>0</r><c>0</c><w>2</w></merge>
<merge><r>1</r><c>0</c><w>2</w></merge>
<namedItem xsi:type="NamedItemCells"><name>Заголовок</name><area><type>Rows</type><beginRow>0</beginRow><endRow>2</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>ШапкаТаблицы</name><area><type>Rows</type><beginRow>3</beginRow><endRow>3</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<namedItem xsi:type="NamedItemCells"><name>Строка</name><area><type>Rows</type><beginRow>4</beginRow><endRow>4</endRow><beginColumn>-1</beginColumn><endColumn>-1</endColumn></area></namedItem>
<line width="1" gap="false"><v8ui:style xsi:type="v8ui:SpreadsheetDocumentCellLineType">Solid</v8ui:style></line>
<format><width>80</width></format>
<format><width>360</width></format>
<format><width>140</width></format>
<format><height>60</height></format>
<format><horizontalAlignment>Left</horizontalAlignment><textPlacement>Wrap</textPlacement><fillType>Template</fillType></format>
<format><horizontalAlignment>Left</horizontalAlignment><textPlacement>Wrap</textPlacement><fillType>Template</fillType></format>
<format><border>0</border><horizontalAlignment>Center</horizontalAlignment><textPlacement>Wrap</textPlacement><fillType>Text</fillType></format>
<format><border>0</border><horizontalAlignment>Right</horizontalAlignment><fillType>Parameter</fillType></format>
<format><border>0</border><horizontalAlignment>Left</horizontalAlignment><textPlacement>Wrap</textPlacement><fillType>Parameter</fillType></format>
<format><width>72</width></format>
</document>
"""


def save_form(writer: Writer, folder, object_name, form_name, synonym, form_xml, bsl_relative):
    descriptor, layout = form_file(f"{folder}/{object_name}/{form_name}", form_name, synonym, form_xml)
    base = f"{folder}/{object_name}/Forms/{form_name}"
    writer.raw(base + ".xml", descriptor)
    writer.raw(base + "/Ext/Form.xml", layout)
    writer.bsl(base + "/Ext/Form/Module.bsl", read_bsl(bsl_relative))


def save_module(writer: Writer, relative_xml_body, xml_path, bsl_path, bsl_relative):
    writer.xml(xml_path, relative_xml_body)
    writer.bsl(bsl_path, read_bsl(bsl_relative))


def build_receipt(root: Path):
    writer = Writer(root)
    name = "УчетПриемкиНаСклад"
    children = [
        ("Language", "Русский"),
        ("Subsystem", "Приемка"),
        ("Role", "ПолныеПрава"),
        ("CommonModule", "ЗагрузкаДемоДанныхСервер"),
        ("CommonModule", "НастройкиСервер"),
        ("CommonModule", "ОбщегоНазначенияСервер"),
        ("CommonModule", "ОтправкаПочтыСервер"),
        ("Constant", "АдресСервераSMTP"),
        ("Constant", "ИспользоватьSSLSMTP"),
        ("Constant", "ЛогинSMTP"),
        ("Constant", "ПарольSMTP"),
        ("Constant", "ПортSMTP"),
        ("Catalog", "Контакты"),
        ("Catalog", "Товары"),
        ("Document", "ПоступлениеТоваровНаСклад"),
        ("DataProcessor", "ЗагрузкаДемоДанных"),
        ("DataProcessor", "НастройкиОтправки"),
        ("DataProcessor", "РабочийСтолКладовщика"),
        ("AccumulationRegister", "ОстаткиТоваров"),
    ]
    writer.raw("Configuration.xml", configuration_xml(
        name,
        "Учет приемки на склад",
        "Учет приемки товаров и отправка PDF-отчета по SMTP.",
        children,
    ))
    writer.bsl("Ext/ManagedApplicationModule.bsl", read_bsl("receipt/ManagedApplicationModule.bsl"))
    writer.xml("Languages/Русский.xml", language_xml())
    writer.xml("Roles/ПолныеПрава.xml", role_xml())
    writer.raw("Roles/ПолныеПрава/Ext/Rights.xml", rights_xml(name))
    writer.xml("Subsystems/Приемка.xml", subsystem_xml("Приемка", "Приемка", [
        "DataProcessor.РабочийСтолКладовщика",
        "DataProcessor.ЗагрузкаДемоДанных",
        "Document.ПоступлениеТоваровНаСклад",
        "Catalog.Товары",
        "Catalog.Контакты",
        "AccumulationRegister.ОстаткиТоваров",
        "DataProcessor.НастройкиОтправки",
        "Constant.АдресСервераSMTP",
        "Constant.ПортSMTP",
        "Constant.ИспользоватьSSLSMTP",
        "Constant.ЛогинSMTP",
        "Constant.ПарольSMTP",
    ]))

    pairs = [
        ("ЗагрузкаДемоДанныхСервер", "Загрузка демо-данных сервер", "receipt/ЗагрузкаДемоДанныхСервер.bsl"),
        ("НастройкиСервер", "Настройки сервер", "receipt/НастройкиСервер.bsl"),
        ("ОбщегоНазначенияСервер", "Общего назначения сервер", "receipt/ОбщегоНазначенияСервер.bsl"),
        ("ОтправкаПочтыСервер", "Отправка почты сервер", "receipt/ОтправкаПочтыСервер.bsl"),
    ]
    for module_name, module_synonym, bsl_name in pairs:
        save_module(
            writer,
            module_xml(module_name, module_synonym),
            f"CommonModules/{module_name}.xml",
            f"CommonModules/{module_name}/Ext/Module.bsl",
            bsl_name,
        )

    writer.xml("Constants/АдресСервераSMTP.xml", constant_xml("АдресСервераSMTP", "Адрес сервера SMTP", type_string(100)))
    writer.xml("Constants/ПортSMTP.xml", constant_xml("ПортSMTP", "Порт SMTP", type_number(5, 0, "Nonnegative")))
    writer.xml("Constants/ИспользоватьSSLSMTP.xml", constant_xml("ИспользоватьSSLSMTP", "Использовать SSL SMTP", type_bool()))
    writer.xml("Constants/ЛогинSMTP.xml", constant_xml("ЛогинSMTP", "Логин SMTP", type_string(100)))
    writer.xml("Constants/ПарольSMTP.xml", constant_xml("ПарольSMTP", "Пароль SMTP", type_string(100), password=True))

    writer.xml("Catalogs/Товары.xml", catalog_xml("Товары", "Товары", 100, [], []))
    writer.xml("Catalogs/Контакты.xml", catalog_xml(
        "Контакты",
        "Контакты",
        100,
        [attribute_xml("Email", "Email", type_string(150), "Контакты.Email", fill="ShowError")],
        [],
    ))

    receipt_attributes = [
        attribute_xml("КомуОтправить", "Кому отправить", type_ref("CatalogRef.Контакты"), "Поступление.КомуОтправить"),
        attribute_xml("АдресЭлектроннойПочты", "Адрес электронной почты", type_string(150), "Поступление.Email"),
        attribute_xml("Комментарий", "Комментарий", type_string(250), "Поступление.Комментарий"),
    ]
    goods_columns = [
        column_xml("Товар", "Товар", type_ref("CatalogRef.Товары"), "Поступление.Товары.Товар", fill="DontCheck"),
        column_xml("Количество", "Количество", type_number(10, 3, "Any"), "Поступление.Товары.Количество"),
    ]
    writer.xml("Documents/ПоступлениеТоваровНаСклад.xml", document_xml(
        "ПоступлениеТоваровНаСклад",
        "Поступление товаров на склад",
        receipt_attributes,
        tabular_section("Document", "ПоступлениеТоваровНаСклад", "Товары", "Товары", goods_columns),
        ["ФормаДокумента"],
        ["ПечатьПоступления"],
        "ОстаткиТоваров",
        "ФормаДокумента",
    ))
    writer.bsl(
        "Documents/ПоступлениеТоваровНаСклад/Ext/ObjectModule.bsl",
        read_bsl("receipt/ObjectModule_Поступление.bsl"),
    )
    writer.xml(
        "Documents/ПоступлениеТоваровНаСклад/Templates/ПечатьПоступления.xml",
        template_meta("ПечатьПоступления", "Печать поступления"),
    )
    writer.raw(
        "Documents/ПоступлениеТоваровНаСклад/Templates/ПечатьПоступления/Ext/Template.xml",
        receipt_template(),
    )

    form = FormBuilder()
    form.attr_object("DocumentObject.ПоступлениеТоваровНаСклад")
    form.command("ОтправитьОтчет", "Отправить отчёт", "КнопкаОтправитьОтчет")
    form.command("ДвиженияДокумента", "Движения документа", "КнопкаДвижения")
    form.event("OnOpen", "ПриОткрытии")
    form.event("AfterWrite", "ПослеЗаписи")
    form.input("Номер", "Объект.Number", on_change="РеквизитПриИзменении")
    form.input("Дата", "Объект.Date", on_change="РеквизитПриИзменении")
    form.input("КомуОтправить", "Объект.КомуОтправить", on_change="КомуОтправитьПриИзменении")
    form.input("АдресЭлектроннойПочты", "Объект.АдресЭлектроннойПочты", on_change="РеквизитПриИзменении")
    form.input("Комментарий", "Объект.Комментарий", on_change="РеквизитПриИзменении")
    form.table(
        "Товары",
        "Объект.Товары",
        [("Товар", "Объект.Товары.Товар"), ("Количество", "Объект.Товары.Количество")],
        on_change="ТоварыПриИзменении",
    )
    save_form(
        writer, "Documents", "ПоступлениеТоваровНаСклад", "ФормаДокумента",
        "Форма документа", form.xml(), "receipt/Form_Поступление.bsl",
    )

    dimension = register_field(
        "Dimension", "Товар", "Товар", type_ref("CatalogRef.Товары"), "Остатки.Товар",
        "<DenyIncompleteValues>true</DenyIncompleteValues><Indexing>Index</Indexing><FullTextSearch>Use</FullTextSearch><UseInTotals>true</UseInTotals>",
    )
    resource = register_field(
        "Resource", "Количество", "Количество", type_number(15, 0, "Nonnegative"), "Остатки.Количество",
        "<Indexing>DontIndex</Indexing><FullTextSearch>Use</FullTextSearch>",
    )
    writer.xml("AccumulationRegisters/ОстаткиТоваров.xml", register_xml(
        "ОстаткиТоваров", "Остатки товаров", "Balances", [resource], [dimension],
    ))

    writer.xml("DataProcessors/ЗагрузкаДемоДанных.xml", processor_xml("ЗагрузкаДемоДанных", "Загрузка демо-данных", "Форма"))
    writer.xml("DataProcessors/НастройкиОтправки.xml", processor_xml("НастройкиОтправки", "Настройки почты", "Форма"))
    writer.xml("DataProcessors/РабочийСтолКладовщика.xml", processor_xml("РабочийСтолКладовщика", "Рабочий стол кладовщика", "Форма"))

    demo = FormBuilder()
    demo.attr_object("DataProcessorObject.ЗагрузкаДемоДанных")
    demo.attr("РезультатЗагрузки", "Результат загрузки", type_string(0))
    demo.command("Загрузить", "Загрузить демо-данные", "КнопкаЗагрузить")
    demo.decoration("Пояснение", "Кнопка создаёт 5 товаров, 3 контакта и 2 проведённых поступления. Повторный запуск не плодит документы.")
    demo.input("РезультатЗагрузки", "РезультатЗагрузки", readonly=True, multiline=True)
    save_form(writer, "DataProcessors", "ЗагрузкаДемоДанных", "Форма", "Форма", demo.xml(), "receipt/Form_Демо.bsl")

    settings = FormBuilder()
    settings.attr_object("DataProcessorObject.НастройкиОтправки")
    settings.attr("АдресСервераSMTP", "Адрес сервера SMTP", type_string(100))
    settings.attr("ПортSMTP", "Порт SMTP", type_number(5, 0, "Nonnegative"))
    settings.attr("ЛогинSMTP", "Логин SMTP", type_string(100))
    settings.attr("ПарольSMTP", "Пароль SMTP", type_string(100))
    settings.attr("ИспользоватьSSLSMTP", "Использовать SSL", type_bool())
    settings.command("ЗаписатьНастройки", "Записать настройки", "КнопкаЗаписать")
    settings.event("OnCreateAtServer", "ПриСозданииНаСервере")
    settings.decoration("Подсказка", "Пример: smtp.yandex.ru, порт 465, флажок SSL. Это пример. Пароль приложения почты, не пароль входа в ящик. Значения пишутся в константы.")
    settings.input("АдресСервераSMTP", "АдресСервераSMTP")
    settings.input("ПортSMTP", "ПортSMTP")
    settings.input("ЛогинSMTP", "ЛогинSMTP")
    settings.input("ПарольSMTP", "ПарольSMTP", password=True)
    settings.check("ИспользоватьSSLSMTP", "ИспользоватьSSLSMTP")
    save_form(writer, "DataProcessors", "НастройкиОтправки", "Форма", "Форма", settings.xml(), "receipt/Form_Настройки.bsl")

    desk = FormBuilder()
    desk.attr_object("DataProcessorObject.РабочийСтолКладовщика")
    desk.command("ЗагрузитьДемо", "Загрузить демо-данные")
    desk.command("НовоеПоступление", "Новое поступление")
    desk.command("СписокПоступлений", "Поступления")
    desk.command("СписокТоваров", "Товары")
    desk.command("СписокКонтактов", "Контакты")
    desk.command("НастройкиПочты", "Настройки почты")
    desk.decoration(
        "Шаги",
        "1. Загрузите демо-данные. 2. Откройте поступление и проведите его. 3. Кнопка «Движения документа» показывает приход. 4. Заполните настройки почты. 5. В проведённом документе без несохранённых правок нажмите «Отправить отчёт».",
    )
    save_form(writer, "DataProcessors", "РабочийСтолКладовщика", "Форма", "Форма", desk.xml(), "receipt/Form_Стол.bsl")


def build_shelf(root: Path):
    writer = Writer(root)
    name = "ЧитательскийДневникПолка"
    children = [
        ("Language", "Русский"),
        ("Subsystem", "Полка"),
        ("Role", "ПолныеПрава"),
        ("CommonModule", "ДневникЧтенияСервер"),
        ("CommonModule", "ЗагрузкаДемоДанныхСервер"),
        ("CommonModule", "ИнтеграцияИИСервер"),
        ("CommonModule", "НастройкиСервер"),
        ("Constant", "АдресСервисаИИ"),
        ("Constant", "КлючAPIИИ"),
        ("Catalog", "ЗаметкиКИсточникам"),
        ("Catalog", "ИсточникиЧтения"),
        ("Document", "СессияЧтения"),
        ("Enum", "ТипыИсточниковЧтения"),
        ("DataProcessor", "ЗагрузкаДемоДанных"),
        ("DataProcessor", "НастройкиСервисаИИ"),
        ("DataProcessor", "РабочийСтолПолка"),
        ("AccumulationRegister", "ПрочитанныеСтраницы"),
    ]
    writer.raw("Configuration.xml", configuration_xml(
        name,
        "Читательский дневник Полка",
        "Дневник чтения: источники, сессии, заметки, прогресс и рекомендация ИИ.",
        children,
    ))
    writer.xml("Languages/Русский.xml", language_xml())
    writer.xml("Roles/ПолныеПрава.xml", role_xml())
    writer.raw("Roles/ПолныеПрава/Ext/Rights.xml", rights_xml(name))
    writer.xml("Subsystems/Полка.xml", subsystem_xml("Полка", "Полка", [
        "DataProcessor.РабочийСтолПолка",
        "DataProcessor.ЗагрузкаДемоДанных",
        "Catalog.ИсточникиЧтения",
        "Catalog.ЗаметкиКИсточникам",
        "Document.СессияЧтения",
        "AccumulationRegister.ПрочитанныеСтраницы",
        "DataProcessor.НастройкиСервисаИИ",
        "Constant.АдресСервисаИИ",
        "Constant.КлючAPIИИ",
    ]))

    for module_name, module_synonym, bsl_name in [
        ("ДневникЧтенияСервер", "Дневник чтения сервер", "shelf/ДневникЧтенияСервер.bsl"),
        ("ЗагрузкаДемоДанныхСервер", "Загрузка демо-данных сервер", "shelf/ЗагрузкаДемоДанныхСервер.bsl"),
        ("ИнтеграцияИИСервер", "Интеграция ИИ сервер", "shelf/ИнтеграцияИИСервер.bsl"),
        ("НастройкиСервер", "Настройки сервер", "shelf/НастройкиСервер.bsl"),
    ]:
        save_module(
            writer,
            module_xml(module_name, module_synonym),
            f"CommonModules/{module_name}.xml",
            f"CommonModules/{module_name}/Ext/Module.bsl",
            bsl_name,
        )

    writer.xml("Constants/АдресСервисаИИ.xml", constant_xml("АдресСервисаИИ", "Адрес сервиса ИИ", type_string(250)))
    writer.xml("Constants/КлючAPIИИ.xml", constant_xml("КлючAPIИИ", "Ключ API ИИ", type_string(500), password=True))
    writer.xml("Enums/ТипыИсточниковЧтения.xml", enum_xml(
        "ТипыИсточниковЧтения",
        "Типы источников чтения",
        [("Книга", "Книга"), ("Статья", "Статья"), ("Учебник", "Учебник")],
    ))

    source_attributes = [
        attribute_xml("Автор", "Автор", type_string(150), "Источник.Автор", fill="ShowError"),
        attribute_xml("ТипИсточника", "Тип", type_ref("EnumRef.ТипыИсточниковЧтения"), "Источник.Тип", fill="ShowError"),
        attribute_xml("ОбщееКоличествоСтраниц", "Общее количество страниц", type_number(5, 0, "Nonnegative"), "Источник.Страницы", fill="ShowError"),
        attribute_xml("Тема", "Тема", type_string(150), "Источник.Тема", fill="ShowError"),
    ]
    writer.xml("Catalogs/ИсточникиЧтения.xml", catalog_xml(
        "ИсточникиЧтения", "Источники чтения", 150, source_attributes, ["ФормаЭлемента"], object_form="ФормаЭлемента",
    ))
    writer.bsl("Catalogs/ИсточникиЧтения/Ext/ObjectModule.bsl", read_bsl("shelf/ObjectModule_ИсточникЧтения.bsl"))

    note_attributes = [
        attribute_xml("НомерСтраницы", "Номер страницы", type_number(5, 0, "Nonnegative"), "Заметка.Страница", fill="ShowError"),
        attribute_xml("ТекстЗаметки", "Текст заметки", type_string(0), "Заметка.Текст", fill="ShowError"),
        attribute_xml("ДатаСоздания", "Дата создания", type_date(), "Заметка.Дата"),
    ]
    writer.xml("Catalogs/ЗаметкиКИсточникам.xml", catalog_xml(
        "ЗаметкиКИсточникам",
        "Заметки к источникам",
        150,
        note_attributes,
        [],
        owners=["Catalog.ИсточникиЧтения"],
        code_series="WithinOwnerSubordination",
    ))
    writer.bsl("Catalogs/ЗаметкиКИсточникам/Ext/ObjectModule.bsl", read_bsl("shelf/ObjectModule_Заметка.bsl"))

    source_form = FormBuilder()
    source_form.attr_object("CatalogObject.ИсточникиЧтения")
    source_form.command("ЗаметкиИсточника", "Заметки", "КнопкаЗаметки")
    source_form.command("ДобавитьЗаметку", "Добавить заметку", "КнопкаДобавитьЗаметку")
    source_form.event("AfterWrite", "ПослеЗаписи")
    source_form.input("Наименование", "Объект.Description")
    source_form.input("Автор", "Объект.Автор")
    source_form.input("ТипИсточника", "Объект.ТипИсточника")
    source_form.input("ОбщееКоличествоСтраниц", "Объект.ОбщееКоличествоСтраниц")
    source_form.input("Тема", "Объект.Тема")
    source_form.decoration("ПояснениеЗаметок", "Заметки этого источника открываются списком подчинённого справочника. В том списке их можно изменить и удалить.")
    save_form(writer, "Catalogs", "ИсточникиЧтения", "ФормаЭлемента", "Форма элемента", source_form.xml(), "shelf/Form_Источник.bsl")

    session_attributes = [
        attribute_xml("ИсточникЧтения", "Источник чтения", type_ref("CatalogRef.ИсточникиЧтения"), "Сессия.Источник", fill="DontCheck"),
        attribute_xml("НачальнаяСтраница", "Начальная страница", type_number(5, 0, "Any"), "Сессия.Начало"),
        attribute_xml("КонечнаяСтраница", "Конечная страница", type_number(5, 0, "Any"), "Сессия.Конец"),
        attribute_xml("ПрочитаноСтраниц", "Прочитано страниц", type_number(5, 0, "Nonnegative"), "Сессия.Прочитано"),
        attribute_xml("Комментарий", "Комментарий", type_string(250), "Сессия.Комментарий"),
    ]
    writer.xml("Documents/СессияЧтения.xml", document_xml(
        "СессияЧтения",
        "Сессия чтения",
        session_attributes,
        "",
        ["ФормаДокумента"],
        [],
        "ПрочитанныеСтраницы",
        "ФормаДокумента",
    ))
    writer.bsl("Documents/СессияЧтения/Ext/ObjectModule.bsl", read_bsl("shelf/ObjectModule_Сессия.bsl"))

    session_form = FormBuilder()
    session_form.attr_object("DocumentObject.СессияЧтения")
    session_form.command("ДвиженияДокумента", "Движения документа", "КнопкаДвижения")
    session_form.event("AfterWrite", "ПослеЗаписи")
    session_form.input("Номер", "Объект.Number")
    session_form.input("Дата", "Объект.Date")
    session_form.input("ИсточникЧтения", "Объект.ИсточникЧтения")
    session_form.input("НачальнаяСтраница", "Объект.НачальнаяСтраница")
    session_form.input("КонечнаяСтраница", "Объект.КонечнаяСтраница")
    session_form.input("ПрочитаноСтраниц", "Объект.ПрочитаноСтраниц", readonly=True)
    session_form.input("Комментарий", "Объект.Комментарий")
    session_form.decoration("ПояснениеФормулы", "Поле «Прочитано страниц» заполняет модуль объекта при записи: конечная страница минус начальная плюс 1.")
    save_form(writer, "Documents", "СессияЧтения", "ФормаДокумента", "Форма документа", session_form.xml(), "shelf/Form_Сессия.bsl")

    resource = register_field(
        "Resource",
        "КоличествоПрочитанныхСтраниц",
        "Количество прочитанных страниц",
        type_number(10, 0, "Nonnegative"),
        "Чтение.Страницы",
        "<Indexing>DontIndex</Indexing><FullTextSearch>Use</FullTextSearch>",
    )
    dimension = register_field(
        "Dimension",
        "ИсточникЧтения",
        "Источник чтения",
        type_ref("CatalogRef.ИсточникиЧтения"),
        "Чтение.Источник",
        "<DenyIncompleteValues>true</DenyIncompleteValues><Indexing>Index</Indexing><FullTextSearch>Use</FullTextSearch><UseInTotals>true</UseInTotals>",
    )
    writer.xml("AccumulationRegisters/ПрочитанныеСтраницы.xml", register_xml(
        "ПрочитанныеСтраницы", "Прочитанные страницы", "Turnovers", [resource], [dimension],
    ))

    writer.xml("DataProcessors/ЗагрузкаДемоДанных.xml", processor_xml("ЗагрузкаДемоДанных", "Загрузка демо-данных", "Форма"))
    writer.xml("DataProcessors/НастройкиСервисаИИ.xml", processor_xml("НастройкиСервисаИИ", "Настройки сервиса ИИ", "Форма"))
    writer.xml("DataProcessors/РабочийСтолПолка.xml", processor_xml("РабочийСтолПолка", "Рабочий стол полки", "Форма"))

    demo = FormBuilder()
    demo.attr_object("DataProcessorObject.ЗагрузкаДемоДанных")
    demo.attr("РезультатЗагрузки", "Результат загрузки", type_string(0))
    demo.command("Загрузить", "Загрузить демо-данные", "КнопкаЗагрузить")
    demo.decoration("Пояснение", "Кнопка создаёт 3 источника, 6 заметок, 6 сессий за последние 7 дней и 2 сессии старше. Повторный запуск не плодит сессии.")
    demo.input("РезультатЗагрузки", "РезультатЗагрузки", readonly=True, multiline=True)
    save_form(writer, "DataProcessors", "ЗагрузкаДемоДанных", "Форма", "Форма", demo.xml(), "shelf/Form_Демо.bsl")

    settings = FormBuilder()
    settings.attr_object("DataProcessorObject.НастройкиСервисаИИ")
    settings.attr("АдресСервисаИИ", "Адрес сервиса ИИ", type_string(250))
    settings.attr("КлючAPIИИ", "Ключ API ИИ", type_string(500))
    settings.command("ЗаписатьНастройки", "Записать настройки", "КнопкаЗаписать")
    settings.event("OnCreateAtServer", "ПриСозданииНаСервере")
    settings.decoration(
        "Подсказка",
        "Если адрес содержит gigachat, модуль сначала получает OAuth-токен, затем вызывает chat/completions. Для другого адреса уходит один POST JSON. Ключ в код не вшит.",
    )
    settings.input("АдресСервисаИИ", "АдресСервисаИИ")
    settings.input("КлючAPIИИ", "КлючAPIИИ", password=True)
    save_form(writer, "DataProcessors", "НастройкиСервисаИИ", "Форма", "Форма", settings.xml(), "shelf/Form_Настройки.bsl")

    desk = FormBuilder()
    desk.attr_object("DataProcessorObject.РабочийСтолПолка")
    desk.attr("КоличествоСессийЗаНеделю", "Сессий за 7 дней", type_number(10, 0, "Nonnegative"))
    desk.attr("СуммаСтраницЗаНеделю", "Страниц за 7 дней", type_number(10, 0, "Nonnegative"))
    desk.attr("СамыйАктивныйИсточник", "Самый активный источник", type_string(150))
    desk.attr("ТекущийИсточникПредставление", "Заметки источника", type_string(150))
    desk.attr("ТекстРекомендации", "Рекомендация", type_string(0))
    desk.attr("ТекстОшибки", "Ошибка", type_string(0))
    desk.attr_table("ТаблицаПрогресса", "Прогресс", [
        ("ИсточникЧтения", "Источник", type_ref("CatalogRef.ИсточникиЧтения")),
        ("НазваниеИсточника", "Название", type_string(150)),
        ("Автор", "Автор", type_string(150)),
        ("ТипИсточника", "Тип", type_ref("EnumRef.ТипыИсточниковЧтения")),
        ("Тема", "Тема", type_string(150)),
        ("ОбщееКоличествоСтраниц", "Всего страниц", type_number(10, 0, "Nonnegative")),
        ("ПрочитаноСтраниц", "Прочитано страниц", type_number(10, 0, "Nonnegative")),
        ("ПроцентЗавершения", "Процент завершения", type_number(10, 1, "Nonnegative")),
        ("ДатаПоследнейСессии", "Дата последней сессии", type_date()),
    ])
    desk.attr_table("Заметки", "Заметки", [
        ("НомерСтраницы", "Страница", type_number(5, 0, "Nonnegative")),
        ("ТекстЗаметки", "Текст заметки", type_string(0)),
        ("ДатаСоздания", "Дата создания", type_date()),
    ])
    desk.command("ОбновитьПрогресс", "Обновить", "КнопкаОбновить")
    desk.command("ЗагрузитьДемо", "Загрузить демо-данные")
    desk.command("СписокИсточников", "Источники")
    desk.command("НоваяСессия", "Новая сессия")
    desk.command("ОткрытьИсточник", "Открыть источник")
    desk.command("НастройкиИИ", "Настройки ИИ")
    desk.command("ЧтоЧитатьДальше", "Что читать дальше?", "КнопкаЧтоЧитатьДальше")
    desk.command("Повторить", "Повторить", "КнопкаПовторить", visible=False)
    desk.event("OnCreateAtServer", "ПриСозданииНаСервере")
    desk.event("NotificationProcessing", "ОбработкаОповещения")
    desk.label("КоличествоСессийЗаНеделю", "КоличествоСессийЗаНеделю")
    desk.label("СуммаСтраницЗаНеделю", "СуммаСтраницЗаНеделю")
    desk.label("СамыйАктивныйИсточник", "СамыйАктивныйИсточник")
    desk.table(
        "ТаблицаПрогресса",
        "ТаблицаПрогресса",
        [
            ("НазваниеИсточника", "ТаблицаПрогресса.НазваниеИсточника"),
            ("Автор", "ТаблицаПрогресса.Автор"),
            ("ТипИсточника", "ТаблицаПрогресса.ТипИсточника"),
            ("Тема", "ТаблицаПрогресса.Тема"),
            ("ОбщееКоличествоСтраниц", "ТаблицаПрогресса.ОбщееКоличествоСтраниц"),
            ("ПрочитаноСтраниц", "ТаблицаПрогресса.ПрочитаноСтраниц"),
            ("ПроцентЗавершения", "ТаблицаПрогресса.ПроцентЗавершения"),
            ("ДатаПоследнейСессии", "ТаблицаПрогресса.ДатаПоследнейСессии"),
        ],
        on_activate="ТаблицаПрогрессаПриАктивизацииСтроки",
    )
    desk.label("ТекущийИсточникПредставление", "ТекущийИсточникПредставление")
    desk.table(
        "Заметки",
        "Заметки",
        [
            ("НомерСтраницы", "Заметки.НомерСтраницы"),
            ("ТекстЗаметки", "Заметки.ТекстЗаметки"),
            ("ДатаСоздания", "Заметки.ДатаСоздания"),
        ],
    )
    desk.input("ТекстРекомендации", "ТекстРекомендации", readonly=True, multiline=True)
    desk.input("ТекстОшибки", "ТекстОшибки", readonly=True, multiline=True)
    save_form(writer, "DataProcessors", "РабочийСтолПолка", "Форма", "Форма", desk.xml(), "shelf/Form_Стол.bsl")


def validate(root: Path):
    errors = []
    for path in root.rglob("*.xml"):
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"{path}: {exc}")
    form_modules = list(root.rglob("Forms/**/Module.bsl"))
    for path in form_modules:
        text = path.read_text(encoding="utf-8-sig")
        if "Новый Запрос" in text or "HTTPСоединение" in text or "86400" in text:
            errors.append(f"form logic in {path}")
    joined = "\n".join(path.read_text(encoding="utf-8-sig") for path in root.rglob("*.bsl"))
    if "86400" in joined:
        errors.append("magic 86400 found")
    if "ЗаметкиКИсточникам" not in (root / "Configuration.xml").read_text(encoding="utf-8"):
        if (root / "Catalogs" / "ЗаметкиКИсточникам.xml").exists() is False and "Полка" in root.name:
            errors.append("notes catalog missing")
    return errors


def main():
    receipt = ROOT / "src" / "УчетПриемкиНаСклад"
    shelf = ROOT / "src" / "ЧитательскийДневникПолка"
    build_receipt(receipt)
    build_shelf(shelf)
    problems = validate(receipt) + validate(shelf)
    notes = shelf / "Catalogs" / "ЗаметкиКИсточникам.xml"
    if "<Catalog" not in notes.read_text(encoding="utf-8"):
        problems.append("notes object is not a catalog")
    if problems:
        print("PROBLEMS")
        print("\n".join(problems))
        return 1
    print("OK", receipt)
    print("OK", shelf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
