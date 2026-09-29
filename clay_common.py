# Shared data + clay illustrations for the app and the poster
import os
# Адрес сайта, на который ведут QR-коды (GitHub Pages)
BASE = os.environ.get("BASE_URL", "https://kerejbajzakov-hue.github.io/maps-project/")
# 1 = вставлять реальные фото из папки photos/, 0 = только иллюстрации
USE_PHOTOS = os.environ.get("PHOTOS", "0") == "1"
VA = "https://www.visitaktobe.kz/ru/guide/page/"

K = dict(  # clay palette
    terra="#E9785C", terraD="#C85A41", terraDD="#8E3A28",
    teal="#57B6CF", tealD="#3893AE",
    gold="#F5C75A", goldD="#D8A43A",
    cream="#FBEEDA", creamD="#EBD5B3",
    green="#8ED3A0", navy="#2F3A5C",
)

# kind: red = мавзолеи и некрополи, blue = мемориальные комплексы (легенда из раздела 4 работы)
DATA = [
 dict(id="abat-baitak", n=1, kind="red", short="Абат-Байтак", name="Мавзолей Абат-Байтак",
      district="Кобдинский район", place="≈12 км к югу от аула Талдысай", period="конец XIV — начало XV века",
      lat=50.095348, lon=55.907836, exact=True, link=VA+"memorialnyj-kompleks-abat-bajta", icon="abat",
      text=["Архитектурный памятник конца XIV — начала XV века на территории некрополя Абат-Байтак.",
            "По народному преданию, мавзолей связан с именем Абат батыра — сына мыслителя и жырау Асан Кайгы.",
            "Исследователи рассматривают памятник как сооружение, связанное с погребением знатного человека."],
      q="С каким мыслителем и жырау предание связывает этот мавзолей?", a="С Асан Кайгы: Абат батыр считается его сыном."),
 dict(id="kobylandy", n=2, kind="blue", short="Кобыланды батыр", name="Мемориальный комплекс «Кобыланды батыр»",
      district="Кобдинский район", place="село Жиренкопа", period="XV век · мавзолей 2007 г.",
      lat=50.848524, lon=54.838053, exact=True, link=VA+"memorialnyj-kompleks-kobylandy-batyr", icon="kob",
      text=["Кобыланды батыр — историческая личность XV века, герой казахского эпоса и народных преданий.",
            "Современный мавзолей построен в 2007 году. Высота около 17,5 м, форма напоминает воинский шлем.",
            "Комплекс посвящён памяти Кобыланды батыра."],
      q="На что похожа форма мавзолея Кобыланды батыра?", a="На воинский шлем. Высота — около 17,5 м."),
 dict(id="eset-kokiuly", n=3, kind="blue", short="Есет Кокиулы", name="Мемориальный комплекс Есета Кокиулы",
      district="Алгинский район", place="село Бестамак", period="XVIII век · мавзолей 1992 г.",
      lat=50.046297, lon=57.400670, exact=True, link=VA+"memorialnyj-kompleks-eseta-kokiuly", icon="eset",
      text=["Мавзолей и некрополь Есета Кокиулы находятся в селе Бестамак.",
            "Есет батыр был одним из известных защитников родной земли и связан с историей Казахского ханства XVIII века.",
            "Мавзолей построен в 1992 году и напоминает традиционную юрту. Рядом работает музей."],
      q="Какое традиционное жилище напоминает мавзолей Есета батыра?", a="Юрту."),
 dict(id="khan-molasy", n=4, kind="blue", short="Хан моласы", name="Мемориальный комплекс «Хан моласы»",
      district="Айтекебийский район", place="Айтекебийский район", period="XVIII век · комплекс 2015 г.",
      lat=49.954875, lon=62.890478, exact=True, link=VA+"han-molasy-memorialdy-kesheni", icon="khan",
      text=["«Хан моласы» — известный исторический и сакральный объект Айтекебийского района.",
            "С этим местом связано захоронение Абулхаир хана, хана Младшего жуза.",
            "В 2015 году создан мемориальный комплекс с памятной стелой и мавзолеем. На некрополе много захоронений."],
      q="Захоронение какого хана связано с «Хан моласы»?", a="Абулхаир хана — хана Младшего жуза."),
 dict(id="kotibar", n=5, kind="red", short="Котибар батыр", name="Мавзолей Котибар батыра Басенулы",
      district="Мугалжарский район", place="≈13 км восточнее села Аккемер", period="мавзолей 2000 г.",
      lat=48.9, lon=57.6, exact=False, link=VA+"mavzolej-kotibar-batyra-basenuly", icon="kot",
      search="Мавзолей Котибар батыра Басенулы",
      text=["Мавзолей Котибар батыра находится примерно в 13 км восточнее села Аккемер.",
            "Высота около 12 м. Построен из ракушечника в 2000 году. Рядом стоят кулпытасы с именами современников и соратников батыра.",
            "Памятник знакомит с историей известных представителей казахского народа и традициями мемориальной архитектуры."],
      q="Из какого материала построен мавзолей Котибар батыра?", a="Из ракушечника. Высота — около 12 м."),
 dict(id="eset-daribay", n=6, kind="red", short="Есет-Дарибай", name="Мавзолей «Есет-Дарибай»",
      district="Шалкарский район", place="Шалкарский район", period="XIX век · 1890 / 1993 гг.",
      lat=47.333494, lon=59.138164, exact=True, link=VA+"mavzolej-eset-daribaya", icon="dar",
      text=["Мавзолей посвящён Есету Котыбарулы, жившему в XIX веке.",
            "Первый мавзолей построили здесь в 1890 году, со временем он разрушился.",
            "Новый мавзолей сооружён в 1993 году."],
      q="В каком году построили первый мавзолей на этом месте?", a="В 1890 году. Новый — в 1993 году."),
 dict(id="kyzyltam", n=7, kind="red", short="Кызылтам", name="Мавзолей Кызылтам",
      district="Каргалинский район", place="у Каргалинского водохранилища", period="позднее средневековье",
      lat=50.55, lon=57.95, exact=False, link=VA+"mavzolej-kyzyltam", icon="kyz",
      search="Мавзолей Кызылтам Каргалинский район",
      text=["Мавзолей Кызылтам стоит в Каргалинском районе, около Каргалинского водохранилища.",
            "Один из редких мавзолеев региона из жжёного кирпича. Относится к эпохе позднего средневековья.",
            "Название «Кызылтам» связано с красноватым цветом кирпича: издалека он похож на красный камень."],
      q="Почему мавзолей называют «Кызылтам»?", a="Из-за красноватого жжёного кирпича, похожего издалека на красный камень."),
]

def filters(prefix=""):
    """Clay filters: soft inner light top-left, inner shade bottom-right. Applied per shape."""
    def f(id_, sd, off, dark=.32, light=.7):
        return f'''<filter id="{prefix}{id_}" x="-15%" y="-15%" width="130%" height="130%" color-interpolation-filters="sRGB">
<feGaussianBlur in="SourceAlpha" stdDeviation="{sd}" result="b"/>
<feOffset in="b" dx="-{off}" dy="-{off*1.3:.1f}" result="u"/><feComposite in="SourceAlpha" in2="u" operator="out" result="rd"/>
<feFlood flood-color="#4A2414" flood-opacity="{dark}"/><feComposite in2="rd" operator="in" result="d"/>
<feOffset in="b" dx="{off}" dy="{off*1.3:.1f}" result="w"/><feComposite in="SourceAlpha" in2="w" operator="out" result="rl"/>
<feFlood flood-color="#FFFFFF" flood-opacity="{light}"/><feComposite in2="rl" operator="in" result="l"/>
<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="d"/><feMergeNode in="l"/></feMerge></filter>'''
    return (f("clay", 5, 5) + f("claySm", 2.5, 2.5) + f("clayBig", 14, 12, .22, .75) +
            f'''<filter id="{prefix}drop" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="6" dy="14" stdDeviation="10" flood-color="#2F3A5C" flood-opacity=".28"/></filter>''')

def icon(name, prefix=""):
    k = K
    c = f'filter="url(#{prefix}clay)"'
    s = f'filter="url(#{prefix}claySm)"'
    I = {
"abat": f'''<rect x="34" y="92" width="140" height="106" rx="20" fill="{k['terra']}" {c}/>
<path d="M60 76 C60 22 144 22 144 76Z" fill="{k['teal']}" {c}/><rect x="58" y="68" width="88" height="30" rx="14" fill="{k['terraD']}" {c}/>
<circle cx="102" cy="24" r="8" fill="{k['gold']}" {s}/>
<rect x="16" y="78" width="88" height="120" rx="22" fill="{k['terra']}" {c}/>
<path d="M38 198 V142 C38 106 82 106 82 142 V198Z" fill="{k['terraDD']}" {s}/>
<rect x="14" y="74" width="92" height="16" rx="8" fill="{k['gold']}" {s}/>''',
"kob": f'''<rect x="34" y="146" width="132" height="52" rx="20" fill="{k['cream']}" {c}/>
<path d="M44 154 C44 84 70 44 100 24 C130 44 156 84 156 154Z" fill="{k['teal']}" {c}/>
<rect x="38" y="134" width="124" height="22" rx="11" fill="{k['gold']}" {s}/>
<path d="M92 32 C94 14 98 4 100 0 C102 4 106 14 108 32Z" fill="{k['gold']}" {s}/>
<path d="M82 198 V178 C82 158 118 158 118 178 V198Z" fill="{k['navy']}" {s}/>''',
"eset": f'''<rect x="18" y="124" width="164" height="74" rx="24" fill="{k['cream']}" {c}/>
<g stroke="{k['terra']}" stroke-width="5" stroke-linecap="round" opacity=".75"><path d="M34 138 L58 184 M58 138 L34 184 M140 138 L164 184 M164 138 L140 184"/></g>
<path d="M10 136 C24 58 176 58 190 136Z" fill="{k['teal']}" {c}/>
<ellipse cx="100" cy="72" rx="24" ry="11" fill="{k['gold']}" {s}/>
<rect x="82" y="148" width="36" height="50" rx="12" fill="{k['terra']}" {s}/>''',
"khan": f'''<rect x="96" y="126" width="96" height="72" rx="20" fill="{k['cream']}" {c}/>
<path d="M102 134 C102 82 186 82 186 134Z" fill="{k['teal']}" {c}/>
<path d="M128 198 V176 C128 156 160 156 160 176 V198Z" fill="{k['navy']}" {s}/>
<path d="M44 196 L50 42 C52 16 74 16 76 42 L82 196Z" fill="{k['gold']}" {c}/>
<rect x="28" y="180" width="70" height="18" rx="9" fill="{k['creamD']}" {s}/>
<circle cx="63" cy="74" r="11" fill="{k['cream']}" {s}/>''',
"kot": f'''<rect x="48" y="106" width="104" height="92" rx="20" fill="{k['cream']}" {c}/>
<path d="M52 114 C52 64 80 34 100 18 C120 34 148 64 148 114Z" fill="{k['cream']}" {c}/>
<circle cx="100" cy="16" r="7" fill="{k['gold']}" {s}/>
<rect x="46" y="100" width="108" height="14" rx="7" fill="{k['terra']}" {s}/>
<path d="M80 198 V156 C80 132 120 132 120 156 V198Z" fill="{k['terraD']}" {s}/>
<rect x="6" y="160" width="22" height="38" rx="11" fill="{k['creamD']}" {s}/><rect x="30" y="170" width="18" height="28" rx="9" fill="{k['creamD']}" {s}/>
<rect x="154" y="166" width="18" height="32" rx="9" fill="{k['creamD']}" {s}/><rect x="174" y="158" width="22" height="40" rx="11" fill="{k['creamD']}" {s}/>''',
"dar": f'''<path d="M95 34 C97 18 99 8 100 0 C101 8 103 18 105 34Z" fill="{k['gold']}" {s}/>
<path d="M56 110 C56 30 144 30 144 110Z" fill="{k['teal']}" {c}/>
<rect x="30" y="98" width="140" height="100" rx="22" fill="{k['cream']}" {c}/>
<rect x="62" y="108" width="76" height="90" rx="18" fill="{k['terra']}" {c}/>
<path d="M78 198 V154 C78 126 122 126 122 154 V198Z" fill="{k['terraDD']}" {s}/>
<rect x="38" y="128" width="16" height="34" rx="8" fill="{k['teal']}" {s}/><rect x="146" y="128" width="16" height="34" rx="8" fill="{k['teal']}" {s}/>''',
"kyz": f'''<rect x="32" y="88" width="136" height="110" rx="22" fill="{k['terra']}" {c}/>
<path d="M44 98 C44 40 156 40 156 98Z" fill="{k['terra']}" {c}/>
<g stroke="{k['terraDD']}" stroke-width="4" stroke-linecap="round" opacity=".35"><path d="M44 118 H156 M44 142 H156 M44 166 H156"/><path d="M70 98 V118 M120 118 V142 M60 142 V166 M140 142 V166 M96 166 V186"/></g>
<path d="M78 198 V156 C78 130 122 130 122 156 V198Z" fill="{k['terraDD']}" {s}/>''',
    }
    return I[name]
