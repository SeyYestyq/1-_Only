# -*- coding: utf-8 -*-
"""Помощники выгрузки конфигурации 1С в файлы XML (формат 2.17)."""

import uuid
from pathlib import Path

VERSION = "2.17"

NS_ATTRS = (
    'xmlns="http://v8.1c.ru/8.3/MDClasses" '
    'xmlns:app="http://v8.1c.ru/8.2/managed-application/core" '
    'xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" '
    'xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" '
    'xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" '
    'xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" '
    'xmlns:style="http://v8.1c.ru/8.1/data/ui/style" '
    'xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" '
    'xmlns:v8="http://v8.1c.ru/8.1/data/core" '
    'xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" '
    'xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" '
    'xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" '
    'xmlns:xen="http://v8.1c.ru/8.3/xcf/enums" '
    'xmlns:xpr="http://v8.1c.ru/8.3/xcf/predef" '
    'xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" '
    'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
)

FORM_NS = (
    'xmlns="http://v8.1c.ru/8.3/xcf/logform" '
    'xmlns:app="http://v8.1c.ru/8.2/managed-application/core" '
    'xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" '
    'xmlns:dcscor="http://v8.1c.ru/8.1/data-composition-system/core" '
    'xmlns:dcssch="http://v8.1c.ru/8.1/data-composition-system/schema" '
    'xmlns:dcsset="http://v8.1c.ru/8.1/data-composition-system/settings" '
    'xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" '
    'xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" '
    'xmlns:style="http://v8.1c.ru/8.1/data/ui/style" '
    'xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" '
    'xmlns:v8="http://v8.1c.ru/8.1/data/core" '
    'xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" '
    'xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" '
    'xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" '
    'xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" '
    'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
)

CLASS_IDS = [
    "9cd510cd-abfc-11d4-9434-004095e12fc7",
    "9fcd25a0-4822-11d4-9414-008048da11f9",
    "e3687481-0a87-462c-a166-9f34594f9bba",
    "9de14907-ec23-4a07-96f0-85521cb6b53b",
    "51f2d5d8-ea4d-4064-8892-82951750031e",
    "e68182ea-4237-4383-967f-90c1e3370bc7",
    "fb282519-d103-4dd3-bc12-cb271d631dfc",
]


def uid(key: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "mirea-1c-2026/" + key))


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def syn(text: str) -> str:
    if not text:
        return "<Synonym/>"
    return (
        "<Synonym><v8:item><v8:lang>ru</v8:lang>"
        f"<v8:content>{esc(text)}</v8:content></v8:item></Synonym>"
    )


def wrap(body: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<MetaDataObject {NS_ATTRS} version=\"{VERSION}\">\n"
        f"{body}\n"
        "</MetaDataObject>\n"
    )


def generated(pairs) -> str:
    chunks = ["<InternalInfo>"]
    for name, category, key in pairs:
        chunks.append(
            f'<xr:GeneratedType name="{name}" category="{category}">'
            f"<xr:TypeId>{uid(key + ':type')}</xr:TypeId>"
            f"<xr:ValueId>{uid(key + ':value')}</xr:ValueId>"
            "</xr:GeneratedType>"
        )
    chunks.append("</InternalInfo>")
    return "".join(chunks)


def type_string(length: int) -> str:
    return (
        "<Type><v8:Type>xs:string</v8:Type><v8:StringQualifiers>"
        f"<v8:Length>{length}</v8:Length><v8:AllowedLength>Variable</v8:AllowedLength>"
        "</v8:StringQualifiers></Type>"
    )


def type_number(digits: int, fraction: int, sign: str = "Any") -> str:
    return (
        "<Type><v8:Type>xs:decimal</v8:Type><v8:NumberQualifiers>"
        f"<v8:Digits>{digits}</v8:Digits>"
        f"<v8:FractionDigits>{fraction}</v8:FractionDigits>"
        f"<v8:AllowedSign>{sign}</v8:AllowedSign>"
        "</v8:NumberQualifiers></Type>"
    )


def type_bool() -> str:
    return "<Type><v8:Type>xs:boolean</v8:Type></Type>"


def type_date(fractions: str = "DateTime") -> str:
    return (
        "<Type><v8:Type>xs:dateTime</v8:Type><v8:DateQualifiers>"
        f"<v8:DateFractions>{fractions}</v8:DateFractions>"
        "</v8:DateQualifiers></Type>"
    )


def type_ref(name: str) -> str:
    return f"<Type><v8:Type>cfg:{name}</v8:Type></Type>"


def attribute_xml(name, synonym, type_xml, key, fill="DontCheck", indexing="DontIndex", password=False):
    return f"""<Attribute uuid="{uid(key)}">
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
{type_xml}
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
<FillFromFillingValue>false</FillFromFillingValue>
<FillValue xsi:nil="true"/>
<FillChecking>{fill}</FillChecking>
<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>
<ChoiceParameterLinks/>
<ChoiceParameters/>
<QuickChoice>Auto</QuickChoice>
<CreateOnInput>Auto</CreateOnInput>
<ChoiceForm/>
<LinkByType/>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
<Indexing>{indexing}</Indexing>
<FullTextSearch>Use</FullTextSearch>
<DataHistory>Use</DataHistory>
</Properties>
</Attribute>"""


def column_xml(name, synonym, type_xml, key, fill="DontCheck"):
    return f"""<Attribute uuid="{uid(key)}">
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
{type_xml}
<PasswordMode>false</PasswordMode>
<Format/>
<EditFormat/>
<ToolTip/>
<MarkNegatives>false</MarkNegatives>
<Mask/>
<MultiLine>false</MultiLine>
<ExtendedEdit>false</ExtendedEdit>
<MinValue xsi:nil="true"/>
<MaxValue xsi:nil="true"/>
<FillChecking>{fill}</FillChecking>
<ChoiceFoldersAndItems>Items</ChoiceFoldersAndItems>
<ChoiceParameterLinks/>
<ChoiceParameters/>
<QuickChoice>Auto</QuickChoice>
<CreateOnInput>Auto</CreateOnInput>
<ChoiceForm/>
<LinkByType/>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
<Indexing>DontIndex</Indexing>
<FullTextSearch>Use</FullTextSearch>
<DataHistory>Use</DataHistory>
</Properties>
</Attribute>"""


def tabular_section(owner_kind, owner, name, synonym, columns):
    internal = generated([
        (f"{owner_kind}TabularSection.{owner}.{name}", "TabularSection", f"{owner}.{name}.ts"),
        (f"{owner_kind}TabularSectionRow.{owner}.{name}", "TabularSectionRow", f"{owner}.{name}.row"),
    ])
    return f"""<TabularSection uuid="{uid(owner + '.' + name)}">
{internal}
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
<ToolTip/>
<FillChecking>DontCheck</FillChecking>
<StandardAttributes>
<xr:StandardAttribute name="LineNumber">
<xr:LinkByType/>
<xr:FillChecking>DontCheck</xr:FillChecking>
<xr:MultiLine>false</xr:MultiLine>
<xr:FillFromFillingValue>false</xr:FillFromFillingValue>
<xr:CreateOnInput>Auto</xr:CreateOnInput>
<xr:MaxValue xsi:nil="true"/>
<xr:ToolTip/>
<xr:ExtendedEdit>false</xr:ExtendedEdit>
<xr:Format/>
<xr:ChoiceForm/>
<xr:QuickChoice>Auto</xr:QuickChoice>
<xr:ChoiceHistoryOnInput>Auto</xr:ChoiceHistoryOnInput>
<xr:EditFormat/>
<xr:PasswordMode>false</xr:PasswordMode>
<xr:DataHistory>Use</xr:DataHistory>
<xr:MarkNegatives>false</xr:MarkNegatives>
<xr:MinValue xsi:nil="true"/>
<xr:Synonym/>
<xr:Comment/>
<xr:FullTextSearch>Use</xr:FullTextSearch>
<xr:ChoiceParameterLinks/>
<xr:FillValue xsi:nil="true"/>
<xr:Mask/>
<xr:ChoiceParameters/>
</xr:StandardAttribute>
</StandardAttributes>
</Properties>
<ChildObjects>
{''.join(columns)}
</ChildObjects>
</TabularSection>"""


def register_field(tag, name, synonym, type_xml, key, extra=""):
    return f"""<{tag} uuid="{uid(key)}">
<Properties>
<Name>{name}</Name>
{syn(synonym)}
<Comment/>
{type_xml}
<PasswordMode>false</PasswordMode>
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
<CreateOnInput>Auto</CreateOnInput>
<ChoiceForm/>
<LinkByType/>
<ChoiceHistoryOnInput>Auto</ChoiceHistoryOnInput>
{extra}
</Properties>
</{tag}>"""


class Writer:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def xml(self, relative: str, body: str):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(wrap(body), encoding="utf-8")

    def raw(self, relative: str, text: str):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def bsl(self, relative: str, text: str):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = text.strip() + "\n"
        path.write_bytes(b"\xef\xbb\xbf" + data.replace("\n", "\r\n").encode("utf-8"))


def form_file(unique_key, form_name, synonym, inner_xml: str):
    body = f"""<Form uuid="{uid('form:' + unique_key)}">
<Properties>
<Name>{form_name}</Name>
{syn(synonym)}
<Comment/>
<FormType>Managed</FormType>
<IncludeHelpInContents>false</IncludeHelpInContents>
<UsePurposes>
<v8:Value xsi:type="app:ApplicationUsePurpose">PlatformApplication</v8:Value>
</UsePurposes>
</Properties>
</Form>"""
    descriptor = wrap(body)
    layout = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<Form {FORM_NS} version=\"{VERSION}\">\n"
        f"{inner_xml}\n"
        "</Form>\n"
    )
    return descriptor, layout


class FormBuilder:
    def __init__(self):
        self.n = 0
        self.children = []
        self.attributes = []
        self.commands = []
        self.events = []
        self.bar = []

    def nid(self) -> int:
        self.n += 1
        return self.n

    def tip(self, name: str) -> str:
        a, b = self.nid(), self.nid()
        return (
            f'<ContextMenu name="{name}КонтекстноеМеню" id="{a}"/>'
            f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{b}"/>'
        )

    def command(self, name, title, button_name=None, visible=True):
        cid = self.nid()
        self.commands.append(
            f'<Command name="{name}" id="{cid}">'
            "<Title><v8:item><v8:lang>ru</v8:lang>"
            f"<v8:content>{esc(title)}</v8:content></v8:item></Title>"
            f"<ToolTip/><Action>{name}</Action>"
            "<CurrentRowUse>DontUse</CurrentRowUse></Command>"
        )
        bid = self.nid()
        vis = "" if visible else "<Visible>false</Visible>"
        bname = button_name or ("Кнопка" + name)
        tip_id = self.nid()
        self.bar.append(
            f'<Button name="{bname}" id="{bid}">'
            f"<Type>CommandBarButton</Type>{vis}"
            f"<CommandName>Form.Command.{name}</CommandName>"
            f'<ExtendedTooltip name="{bname}РасширеннаяПодсказка" id="{tip_id}"/>'
            "</Button>"
        )

    def event(self, xml_name, procedure):
        self.events.append(f'<Event name="{xml_name}">{procedure}</Event>')

    def input(self, name, path, on_change=None, readonly=False, password=False, multiline=False):
        iid = self.nid()
        extra = ""
        if readonly:
            extra += "<ReadOnly>true</ReadOnly>"
        if password:
            extra += "<PasswordMode>true</PasswordMode>"
        if multiline:
            extra += "<MultiLine>true</MultiLine><Height>4</Height>"
        if on_change:
            extra += f'<Events><Event name="OnChange">{on_change}</Event></Events>'
        self.children.append(
            f'<InputField name="{name}" id="{iid}">'
            f"<DataPath>{path}</DataPath>"
            f"{extra}{self.tip(name)}</InputField>"
        )

    def check(self, name, path):
        iid = self.nid()
        self.children.append(
            f'<CheckBoxField name="{name}" id="{iid}">'
            f"<DataPath>{path}</DataPath>"
            "<CheckBoxType>Auto</CheckBoxType>"
            f"{self.tip(name)}</CheckBoxField>"
        )

    def label(self, name, path):
        iid = self.nid()
        self.children.append(
            f'<LabelField name="{name}" id="{iid}">'
            f"<DataPath>{path}</DataPath>"
            f"{self.tip(name)}</LabelField>"
        )

    def decoration(self, name, text):
        iid = self.nid()
        self.children.append(
            f'<LabelDecoration name="{name}" id="{iid}">'
            '<Title formatted="false"><v8:item><v8:lang>ru</v8:lang>'
            f"<v8:content>{esc(text)}</v8:content></v8:item></Title>"
            f"{self.tip(name)}</LabelDecoration>"
        )

    def table(self, name, path, columns, on_activate=None, on_change=None):
        tid = self.nid()
        cols = []
        for col_name, col_path in columns:
            cid = self.nid()
            cols.append(
                f'<InputField name="{name}{col_name}" id="{cid}">'
                f"<DataPath>{col_path}</DataPath>"
                "<EditMode>EnterOnInput</EditMode>"
                f"{self.tip(name + col_name)}</InputField>"
            )
        events = ""
        ev = []
        if on_activate:
            ev.append(f'<Event name="OnActivateRow">{on_activate}</Event>')
        if on_change:
            ev.append(f'<Event name="OnChange">{on_change}</Event>')
        if ev:
            events = "<Events>" + "".join(ev) + "</Events>"
        bar_id = self.nid()
        self.children.append(
            f'<Table name="{name}" id="{tid}"><Representation>List</Representation>'
            f"<DataPath>{path}</DataPath>"
            f'<ContextMenu name="{name}КонтекстноеМеню" id="{self.nid()}"/>'
            f'<AutoCommandBar name="{name}КоманднаяПанель" id="{bar_id}"/>'
            f'<ExtendedTooltip name="{name}РасширеннаяПодсказка" id="{self.nid()}"/>'
            f"<ChildItems>{''.join(cols)}</ChildItems>"
            f"{events}</Table>"
        )

    def attr_object(self, type_name):
        self.attributes.append(
            f'<Attribute name="Объект" id="{self.nid()}">'
            f"<Type><v8:Type>cfg:{type_name}</v8:Type></Type>"
            "<MainAttribute>true</MainAttribute>"
            "<SavedData>true</SavedData></Attribute>"
        )

    def attr(self, name, title, type_xml):
        self.attributes.append(
            f'<Attribute name="{name}" id="{self.nid()}">'
            "<Title><v8:item><v8:lang>ru</v8:lang>"
            f"<v8:content>{esc(title)}</v8:content></v8:item></Title>"
            f"{type_xml}</Attribute>"
        )

    def attr_table(self, name, title, columns):
        cols = []
        for col_name, col_title, type_xml in columns:
            cols.append(
                f'<Column name="{col_name}" id="{self.nid()}">'
                "<Title><v8:item><v8:lang>ru</v8:lang>"
                f"<v8:content>{esc(col_title)}</v8:content></v8:item></Title>"
                f"{type_xml}</Column>"
            )
        self.attributes.append(
            f'<Attribute name="{name}" id="{self.nid()}">'
            "<Title><v8:item><v8:lang>ru</v8:lang>"
            f"<v8:content>{esc(title)}</v8:content></v8:item></Title>"
            "<Type><v8:Type>v8:ValueTable</v8:Type></Type>"
            f"<Columns>{''.join(cols)}</Columns></Attribute>"
        )

    def xml(self) -> str:
        events = ""
        if self.events:
            events = "<Events>" + "".join(self.events) + "</Events>"
        bar = (
            '<AutoCommandBar name="ФормаКоманднаяПанель" id="-1">'
            "<Autofill>true</Autofill>"
            f"<ChildItems>{''.join(self.bar)}</ChildItems>"
            "</AutoCommandBar>"
        )
        return (
            bar
            + events
            + "<ChildItems>"
            + "".join(self.children)
            + "</ChildItems><Attributes>"
            + "".join(self.attributes)
            + "</Attributes><Commands>"
            + "".join(self.commands)
            + "</Commands>"
        )
