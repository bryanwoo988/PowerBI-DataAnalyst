from kit import *

PBI = "https://learn.microsoft.com/en-us/power-bi/"
DAX = "https://learn.microsoft.com/en-us/dax/"

STAGE = {
    "n": 3, "id": "model", "weight": "25–30%",
    "title": T("Model the data", "数据建模"),
    "blurb": T("Star schema, relationships, a date table, DAX measures, time intelligence and model performance.",
               "星型架构、关系、日期表、DAX 度量值、时间智能和模型性能。"),
    "url": "https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/pl-300",
}

c06 = module("c06", ("Design and implement a data model", "设计和实现数据模型"), [
    lesson("star-schema", ("The star schema", "星型架构"), 7, [
        ("A star schema puts fact tables in the centre and dimension tables around them, each related one-to-many.",
         "星型架构把事实表放在中心，维度表围绕四周，彼此以一对多关系连接。"),
        ("Filters flow from the \"one\" side (dimension) to the \"many\" side (fact).",
         "筛选从「一」端（维度表）流向「多」端（事实表）。"),
        ("Avoid one big flat table and avoid snowflakes of chained dimensions: the star is simpler and faster.",
         "避免一张大扁平表，也避免多层串接的雪花型维度：星型更简单、更快。"),
    ], [
        FIG("img/star-schema.svg", ("Star schema: Sales in the centre related to Date, Product, Customer and Store", "星型架构：Sales 在中心，关联 Date、Product、Customer 和 Store"),
            ("A star schema. Each dimension (1) filters the fact table (*).", "星型架构。每张维度表（1）筛选事实表（*）。")),
        P("Power BI's engine and DAX are designed around the <b>star schema</b>. Slicers and axes come from the dimension tables; the numbers you add up live in the fact table. One relationship per dimension, each <b>one-to-many</b> with a <b>single</b> cross-filter direction from dimension to fact.",
          "Power BI 的引擎和 DAX 都是围绕<b>星型架构</b>设计的。切片器和轴来自维度表；要汇总的数字放在事实表中。每张维度表一个关系，都是<b>一对多</b>，筛选方向为从维度表到事实表的<b>单向</b>。"),
        TABLE([("Design", "设计"), ("Problem", "问题")], [
            [("One flat table with everything", "所有内容放在一张扁平表"), ("Repeats descriptive text on every row (big model), hard to add a second fact table, awkward time intelligence", "每一行都重复描述文字（模型大），难以加入第二张事实表，时间智能也难做")],
            [("Snowflake (Product → Subcategory → Category)", "雪花型（Product → Subcategory → Category）"), ("Longer filter paths, more tables to understand; flatten the chain into one Product dimension in Power Query", "筛选路径更长、要理解的表更多；应在 Power Query 中把这串表展平成一个 Product 维度表")],
            [("Star", "星型"), ("Small, fast, easy to read; the recommended design", "小、快、易读；推荐的设计")],
        ]),
        P("Two fact tables (for example Sales and Budget) can share the same dimensions. These <b>conformed</b> dimensions let one slicer filter both facts at once.",
          "两张事实表（例如 Sales 和 Budget）可以共用相同的维度表。这种<b>一致性</b>维度表让一个切片器同时筛选两张事实表。"),
        Q("Product, Subcategory and Category are three related tables. What does Microsoft guidance recommend for a Power BI model?",
          "Product、Subcategory 和 Category 是三张相互关联的表。对 Power BI 模型，Microsoft 指南建议怎么做？",
          O(True, "Merge them into one Product dimension (denormalise)", "把它们合并成一个 Product 维度表（反规范化）", "Right: a star with one Product table is simpler and faster.", "对：只有一张 Product 表的星型更简单、更快。"),
          O(False, "Keep the snowflake as it is", "保持雪花型不变", "It works, but adds filter hops and complexity.", "可以运作，但会增加筛选跳转和复杂度。"),
          O(False, "Merge them into the Sales fact table", "把它们合并进 Sales 事实表", "That repeats text on every sales row.", "这会在每一行销售记录中重复文字。"),
          O(False, "Relate each one to Sales directly", "让每一张都直接关联 Sales", "Sales only holds the ProductID.", "Sales 中只有 ProductID。")),
    ], terms=["star-schema", "fact-table", "dimension-table", "snowflake"], url=PBI + "guidance/star-schema"),

    lesson("relationships", ("Relationships: cardinality and cross-filter direction", "关系：基数与交叉筛选方向"), 10, [
        ("Cardinality can be one-to-many, many-to-one, one-to-one or many-to-many; one-to-many is the normal case.",
         "基数可以是一对多、多对一、一对一或多对多；一对多是最常见的情况。"),
        ("Cross-filter direction Single filters from the one side to the many side; Both also filters back — use it sparingly.",
         "交叉筛选方向「单向」从「一」端筛选到「多」端；「双向」也会反向筛选——要谨慎使用。"),
        ("Only one active relationship can exist between two tables; others are inactive (dashed) and used with USERELATIONSHIP.",
         "两张表之间只能有一个活动关系；其他关系为非活动（虚线），需用 USERELATIONSHIP 启用。"),
    ], [
        TABLE([("Cardinality", "基数"), ("Meaning", "含义"), ("Example", "例子")], [
            [("One-to-many (1:*)", "一对多（1:*）"), ("Each key appears once on one side, many times on the other", "键在一端只出现一次，在另一端出现多次"), ("Product → Sales", "Product → Sales")],
            [("One-to-one (1:1)", "一对一（1:1）"), ("Unique on both sides; often means the tables should be merged", "两端都唯一；通常表示两张表应该合并"), ("Employee → EmployeeDetails", "Employee → EmployeeDetails")],
            [("Many-to-many (*:*)", "多对多（*:*）"), ("Neither side unique; use carefully, totals may surprise", "两端都不唯一；要小心使用，合计可能出乎意料"), ("Sales (by month) ↔ Budget (by month and category)", "Sales（按月）↔ Budget（按月和类别）")],
        ]),
        H("Cross-filter direction", "交叉筛选方向"),
        FIG("img/filter-direction.svg", ("Single direction: Product filters Sales. Both: Sales also filters Product.", "单向：Product 筛选 Sales。双向：Sales 也筛选 Product。"),
            ("Single (top) is the default for one-to-many. Both (bottom) lets the fact table filter the dimension too.", "单向（上）是一对多的默认值。双向（下）让事实表也能筛选维度表。")),
        UL(("<b>Single</b>: the dimension filters the fact. A slicer on Product[Colour] filters Sales.",
            "<b>单向</b>：维度表筛选事实表。Product[Colour] 切片器会筛选 Sales。"),
           ("<b>Both</b>: the fact also filters the dimension, e.g. a Customer slicer that shows only customers who bought the selected product. It can create ambiguous paths and slows queries.",
            "<b>双向</b>：事实表也会筛选维度表，例如 Customer 切片器只显示购买了所选产品的客户。它可能造成路径不明确，并拖慢查询。"),
           ("Prefer a measure-based fix for one visual: <code>CALCULATE([Sales], CROSSFILTER(Sales[CustomerID], Customer[CustomerID], BOTH))</code>, or filter a slicer with a measure (\"show items where [Sales] is not blank\").",
            "如果只是一个视觉对象需要，优先用度量值解决：<code>CALCULATE([Sales], CROSSFILTER(Sales[CustomerID], Customer[CustomerID], BOTH))</code>，或用度量值筛选切片器（「只显示 [Sales] 不为空的项目」）。")),
        H("Active and inactive relationships", "活动与非活动关系"),
        P("Between two tables only one relationship can be <b>active</b> (solid line). A second one, for example Sales[ShipDate] → Date[Date] next to the active Sales[OrderDate] → Date[Date], is <b>inactive</b> (dashed line). Turn it on inside one measure with USERELATIONSHIP:",
          "两张表之间只能有一个<b>活动</b>关系（实线）。第二个关系，例如在活动的 Sales[OrderDate] → Date[Date] 之外再加 Sales[ShipDate] → Date[Date]，就是<b>非活动</b>关系（虚线）。在度量值中用 USERELATIONSHIP 启用它："),
        CODE('''
Sales by Ship Date =
CALCULATE (
    [Total Sales],
    USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] )
)
'''),
        Q("A Date table is related to Sales[OrderDate] (active) and Sales[DueDate] (inactive). Which DAX activates the second relationship in a measure?",
          "Date 表与 Sales[OrderDate]（活动）和 Sales[DueDate]（非活动）相关。哪个 DAX 能在度量值中启用第二个关系？",
          O(True, "USERELATIONSHIP inside CALCULATE", "在 CALCULATE 中使用 USERELATIONSHIP", "Right: it activates the inactive relationship for that calculation only.", "对：只在这个计算中启用该非活动关系。"),
          O(False, "RELATED", "RELATED", "RELATED fetches a value over an existing active relationship.", "RELATED 是通过现有的活动关系取得值。"),
          O(False, "CROSSFILTER", "CROSSFILTER", "CROSSFILTER changes direction, not which relationship is active.", "CROSSFILTER 改变方向，不改变哪个关系是活动的。"),
          O(False, "TREATAS on its own", "单独使用 TREATAS", "TREATAS applies a virtual relationship, a different technique.", "TREATAS 套用虚拟关系，是另一种技巧。")),
        Q("What is the default cross-filter direction of a new one-to-many relationship?",
          "新建立的一对多关系，默认的交叉筛选方向是什么？",
          O(True, "Single, from the one side to the many side", "单向，从「一」端到「多」端", "", ""),
          O(False, "Both", "双向", "Both is the default for one-to-one relationships, not for one-to-many.", "双向是一对一关系的默认值，不是一对多的。"),
          O(False, "None", "无", "", ""),
          O(False, "From the many side to the one side", "从「多」端到「一」端", "", "")),
    ], terms=["cardinality", "cross-filter-direction", "inactive-relationship"], url=PBI + "transform-model/desktop-relationships-understand"),

    lesson("role-playing", ("Role-playing dimensions", "角色扮演维度"), 6, [
        ("A role-playing dimension is one dimension used for several roles, such as Order Date, Ship Date and Due Date.",
         "角色扮演维度是同一个维度表扮演多种角色，例如订单日期、发货日期和到期日期。"),
        ("Option 1: one table with one active and several inactive relationships, plus USERELATIONSHIP measures.",
         "方法一：一张表，一个活动关系加几个非活动关系，再配合 USERELATIONSHIP 度量值。"),
        ("Option 2: a copy of the dimension per role (reference query or calculated table), each with its own active relationship.",
         "方法二：为每个角色复制一份维度表（引用查询或计算表），各自有活动关系。"),
    ], [
        P("Sales has an OrderDate, a ShipDate and a DueDate. All three describe dates, so they all relate to the Date dimension — the dimension plays three <b>roles</b>.",
          "Sales 有 OrderDate、ShipDate 和 DueDate。三者都是日期，所以都关联到 Date 维度表——这个维度表扮演了三种<b>角色</b>。"),
        TABLE([("", ""), ("Inactive relationships + USERELATIONSHIP", "非活动关系 + USERELATIONSHIP"), ("One table per role", "每个角色一张表")], [
            [("Model size", "模型大小"), ("Smallest: one date table", "最小：一张日期表"), ("Bigger: copies of the table", "较大：表有多个副本")],
            [("Report use", "报表使用"), ("A measure per role (Sales by Ship Date…)", "每个角色一个度量值（按发货日期的销售……）"), ("Users pick 'Ship Date'[Year] directly; can show order and ship dates side by side", "用户直接选择 'Ship Date'[Year]；可以并排显示订单日期和发货日期")],
            [("Best when", "最适合"), ("Few measures need the other roles", "只有少数度量值需要其他角色"), ("Users slice by several roles freely", "用户要自由地按多种角色切片")],
        ]),
        CODE('''
// Calculated table: a second date table for the Ship Date role
Ship Date = 'Date'
'''),
        NOTE("key", "Rename copied columns (Ship Year, Ship Month) so report users can tell the roles apart.",
             "把复制表的列改名（Ship Year、Ship Month），让报表用户能分辨不同角色。"),
        Q("Report users want a matrix with order year on rows and ship year on columns. Which design supports this?",
          "报表用户想要一个矩阵，行是订单年份，列是发货年份。哪种设计能做到？",
          O(True, "Separate Order Date and Ship Date tables, each with an active relationship", "分开的 Order Date 和 Ship Date 表，各有活动关系", "Right: both roles must filter at the same time, which needs two active paths.", "对：两个角色必须同时筛选，所以需要两条活动路径。"),
          O(False, "One Date table with an inactive ShipDate relationship", "一张 Date 表加一个非活动的 ShipDate 关系", "Only one role can be on the axis from a single table.", "一张表只能把一种角色放在轴上。"),
          O(False, "A bidirectional relationship", "双向关系", "", ""),
          O(False, "A many-to-many relationship", "多对多关系", "", "")),
    ], terms=["role-playing-dimension", "inactive-relationship"], url=PBI + "guidance/star-schema"),

    lesson("date-table", ("A common date table", "通用日期表"), 8, [
        ("Time intelligence needs a date table with one row per day, no gaps, covering whole years.",
         "时间智能需要一张日期表：每天一行、没有缺口、涵盖完整年份。"),
        ("Create it in Power Query, with DAX CALENDAR or CALENDARAUTO, or import it from the data warehouse — then Mark as date table.",
         "可在 Power Query 中建立、用 DAX 的 CALENDAR 或 CALENDARAUTO 建立，或从数据仓库导入——然后「标记为日期表」。"),
        ("Turn off Auto date/time for real models: it adds a hidden date table for every date column.",
         "正式的模型应关闭「自动日期/时间」：它会为每个日期列加一张隐藏的日期表。"),
    ], [
        P("Every model with dates needs one <b>common date table</b> that all fact tables share. It lets one Year slicer filter Sales, Budget and Inventory together, and it is required for DAX time intelligence functions to work reliably.",
          "每个含日期的模型都需要一张所有事实表共用的<b>通用日期表</b>。它让一个年份切片器同时筛选 Sales、Budget 和 Inventory，也是 DAX 时间智能函数可靠运作的前提。"),
        UL(("One row per date, <b>no missing days</b>, starting on 1 January (or the fiscal-year start) of the first year and ending on the last day of the last year.",
            "每个日期一行、<b>不缺日期</b>，从第一年的 1 月 1 日（或财年开始日）到最后一年的最后一天。"),
           ("A column of type Date with unique values — the key.", "一个「日期」类型、值唯一的列——作为键。"),
           ("Attribute columns: Year, Quarter, Month number, Month name, Week, Day of week, Fiscal year…", "属性列：年、季度、月份编号、月份名称、周、星期、财年……"),
           ("<b>Mark as date table</b> (Table tools) and choose the date column. Power BI then validates it and stops creating auto date tables for it.",
            "<b>标记为日期表</b>（表工具），并选择日期列。Power BI 会验证它，并不再为其建立自动日期表。")),
        CODE('''
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2022, 1, 1 ), DATE ( 2026, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "Quarter", "Q" & QUARTER ( [Date] )
)
'''),
        TABLE([("Function", "函数"), ("What it returns", "返回")], [
            [("<code>CALENDAR(start, end)</code>", "<code>CALENDAR(start, end)</code>"), ("Every date between two dates you choose", "两个指定日期之间的每一天")],
            [("<code>CALENDARAUTO()</code>", "<code>CALENDARAUTO()</code>"), ("Whole years covering every date found in the model (optional fiscal year-end month)", "涵盖模型中所有日期的完整年份（可选财年结束月份）")],
        ]),
        NOTE("caution", "Remember to set <b>Sort by column</b>: Month name sorted by Month number, otherwise months appear alphabetically (Apr, Aug, Dec…).",
             "记得设定<b>按列排序</b>：月份名称按月份编号排序，否则月份会按字母顺序出现（Apr、Aug、Dec……）。"),
        Q("Your Date table was built from the distinct order dates in Sales, so it has gaps on days without orders. What goes wrong?",
          "你的 Date 表是用 Sales 中不重复的订单日期建立的，所以没有订单的日子会有缺口。会出什么问题？",
          O(True, "Time intelligence functions can return wrong or no results", "时间智能函数可能返回错误结果或没有结果", "Right: they need a complete, contiguous range of dates.", "对：它们需要完整、连续的日期范围。"),
          O(False, "Relationships cannot be created", "无法建立关系", "", ""),
          O(False, "Slicers stop working", "切片器失效", "", ""),
          O(False, "Nothing; gaps are fine", "没问题，有缺口也可以", "", "")),
        Q("Months show in alphabetical order on a chart axis. How do you fix it?",
          "图表轴上的月份按字母顺序显示。怎么修正？",
          O(True, "Sort the Month name column by the Month number column", "把月份名称列设为按月份编号列排序", "Right: Sort by column in Column tools.", "对：在「列工具」中使用「按列排序」。"),
          O(False, "Change Month to a Date type", "把月份改为日期类型", "", ""),
          O(False, "Sort the visual descending", "把视觉对象设为降序排序", "", ""),
          O(False, "Turn on Auto date/time", "开启「自动日期/时间」", "", "")),
    ], terms=["date-table", "mark-as-date-table", "auto-date-time", "sort-by-column"], url=PBI + "guidance/model-date-tables"),

    lesson("properties", ("Table and column properties", "表和列的属性"), 7, [
        ("Hide keys and technical columns; show users only what they should drag into visuals.",
         "隐藏键和技术性的列；只让用户看到应该拖进视觉对象的内容。"),
        ("Set data categories (City, Country, Latitude, URL, Image URL) so maps and links work.",
         "设定数据类别（城市、国家/地区、纬度、网址、图像网址），让地图和链接正常运作。"),
        ("Set Summarize by to Don't summarize for numbers that must not be added up, such as Year or IDs.",
         "对不应相加的数字（如年份或 ID）把「汇总依据」设为「不汇总」。"),
    ], [
        P("A good model is easy to use. The <b>Properties</b> pane in Model view and <b>Column tools</b> in Table view control how each table and column behaves in reports.",
          "好的模型要容易使用。模型视图的<b>属性</b>窗格和表视图的<b>列工具</b>决定每张表和每个列在报表中的表现。"),
        TABLE([("Property", "属性"), ("Use", "用途")], [
            [("Name and description", "名称和说明"), ("Friendly names (\"Sales Amount\" not \"SLS_AMT\"); descriptions show as tooltips in the Data pane", "友好名称（「销售金额」而不是「SLS_AMT」）；说明会在「数据」窗格中显示为工具提示")],
            [("Is hidden", "已隐藏"), ("Hide keys, sort columns and helper columns", "隐藏键、排序用的列和辅助列")],
            [("Data type and format", "数据类型和格式"), ("Currency, percentage, thousands separator, date format", "货币、百分比、千位分隔符、日期格式")],
            [("Data category", "数据类别"), ("Address, City, Country/Region, Postal code, Latitude, Longitude, Web URL, Image URL, Barcode", "地址、城市、国家/地区、邮政编码、纬度、经度、Web URL、图像 URL、条形码")],
            [("Summarize by (default summarization)", "汇总依据（默认汇总）"), ("Sum, Average, Count… or Don't summarize", "求和、平均值、计数……或不汇总")],
            [("Sort by column", "按列排序"), ("Month name by month number, size \"S, M, L\" by a size order", "月份名称按月份编号；尺寸「S、M、L」按尺寸顺序")],
            [("Display folder", "显示文件夹"), ("Group many measures into folders", "把大量度量值分组到文件夹")],
            [("Hierarchy", "层次结构"), ("Year → Quarter → Month for drill-down", "年 → 季度 → 月，用于向下钻取")],
            [("Synonyms", "同义词"), ("Help Q&A and Copilot understand \"revenue\" means Sales Amount", "帮助问答和 Copilot 理解「revenue」就是销售金额")],
        ]),
        EXAM("A common trap: a Year column is summed (\"2,024,000\") in a visual. The fix is Summarize by → Don't summarize (or make the column Text).",
             "常见陷阱：年份列在视觉对象中被加总成「2,024,000」。解决办法是「汇总依据 → 不汇总」（或把列改为文本）。"),
        Q("A column holds website addresses and must appear as clickable links in a table visual. What do you set?",
          "某列存放网址，必须在表格视觉对象中显示为可点击的链接。要设定什么？",
          O(True, "Data category: Web URL", "数据类别：Web URL", "Right; then turn on URL icon in the table's formatting if you want an icon.", "对；若想显示图标，再在表格格式中开启 URL 图标。"),
          O(False, "Data type: Text", "数据类型：文本", "It already is text; the category makes it a link.", "它本来就是文本；类别才会让它变成链接。"),
          O(False, "Summarize by: Don't summarize", "汇总依据：不汇总", "", ""),
          O(False, "A hierarchy", "层次结构", "", "")),
    ], terms=["data-category", "default-summarization", "sort-by-column", "hierarchy"], url=PBI + "transform-model/desktop-data-categorization"),

    lesson("calculated-columns-tables", ("When to use calculated columns and tables", "何时使用计算列和计算表"), 7, [
        ("A calculated column is computed row by row at refresh and stored; use it when you need to slice, filter or group by the result.",
         "计算列在刷新时逐行计算并存储；当你需要按结果切片、筛选或分组时使用。"),
        ("A measure is computed at query time for the current filters; use it for anything you aggregate.",
         "度量值在查询时按当前筛选条件计算；凡是要汇总的都用度量值。"),
        ("Calculated tables suit date tables, role-playing copies and small helper tables built from the model.",
         "计算表适用于日期表、角色扮演副本，以及由模型生成的小型辅助表。"),
    ], [
        TABLE([("", ""), ("Calculated column", "计算列"), ("Measure", "度量值")], [
            [("Computed", "何时计算"), ("At refresh, once per row", "刷新时，每行一次"), ("At query time, per cell of a visual", "查询时，针对视觉对象的每个单元格")],
            [("Stored", "是否存储"), ("Yes — uses memory", "是——占用内存"), ("No", "否")],
            [("Context", "上下文"), ("Row context (sees the current row)", "行上下文（能看到当前行）"), ("Filter context (sees the current filters)", "筛选上下文（能看到当前筛选）")],
            [("Use for", "用于"), ("Slicers, axes, filters, grouping: Age Band, Full Name, Is Weekend", "切片器、轴、筛选、分组：年龄段、全名、是否周末"), ("Numbers to aggregate: Total Sales, Margin %, YoY", "要汇总的数字：总销售额、利润率、同比")],
        ]),
        NOTE("key", "If a column can be created in Power Query instead, prefer Power Query: it compresses better and keeps logic in one place. Use DAX calculated columns when the formula needs other model tables (RELATED) or DAX-only functions.",
             "如果某列也能在 Power Query 中建立，优先用 Power Query：压缩效果更好，逻辑也集中在一处。当公式需要其他模型表（RELATED）或只有 DAX 才有的函数时，再用 DAX 计算列。"),
        CODE('''
// Calculated column on Sales: needs a value from the Product table
Margin = Sales[Amount] - Sales[Quantity] * RELATED ( Product[Standard Cost] )

// Calculated table: customers with sales, for a helper slicer
Active Customers = DISTINCT ( Sales[CustomerID] )
'''),
        Q("Users want to slice sales by price band (Budget, Standard, Premium). Should Price Band be a measure or a column?",
          "用户想按价格段（低价、标准、高价）切片销售数据。价格段该是度量值还是列？",
          O(True, "A column (Power Query or calculated column)", "列（Power Query 或计算列）", "Right: slicers and axes need stored column values.", "对：切片器和轴需要存储的列值。"),
          O(False, "A measure", "度量值", "Measures cannot be placed in a slicer or on an axis.", "度量值不能放进切片器，也不能放在轴上。"),
          O(False, "A calculated table", "计算表", "", ""),
          O(False, "A visual-level filter", "视觉对象级筛选器", "", "")),
    ], terms=["calculated-column", "measure", "calculated-table", "row-context"], url=PBI + "transform-model/desktop-calculated-columns"),
], url=PBI + "transform-model/desktop-modeling-view")

c07 = module("c07", ("DAX essentials", "DAX 基础"), [
    lesson("measures", ("Single aggregation measures", "单一聚合度量值"), 7, [
        ("Write explicit measures (Total Sales = SUM(Sales[Amount])) instead of relying on implicit summarisation of columns.",
         "编写显式度量值（Total Sales = SUM(Sales[Amount])），不要依赖列的隐式汇总。"),
        ("COUNT counts non-blank values in a column; COUNTROWS counts rows of a table; DISTINCTCOUNT counts different values.",
         "COUNT 计算列中的非空值；COUNTROWS 计算表的行数；DISTINCTCOUNT 计算不同值的数量。"),
        ("Build measures on measures: Margin % = DIVIDE([Margin], [Total Sales]).",
         "用度量值构建度量值：Margin % = DIVIDE([Margin], [Total Sales])。"),
    ], [
        P("Dragging a numeric column into a visual creates an <b>implicit measure</b> (the Σ sum). It works, but you cannot reuse it, it does not work with calculation groups, and other tools (Excel, Copilot) see less meaning. Good models use <b>explicit measures</b> written in DAX and hide the raw numeric columns.",
          "把数值列拖进视觉对象会产生<b>隐式度量值</b>（Σ 求和）。它能用，但无法重用、不支持计算组，其他工具（Excel、Copilot）也难以理解。好的模型用 DAX 编写<b>显式度量值</b>，并隐藏原始数值列。"),
        CODE('''
Total Sales    = SUM ( Sales[Amount] )
Order Count    = DISTINCTCOUNT ( Sales[OrderID] )
Sales Lines    = COUNTROWS ( Sales )
Average Price  = AVERAGE ( Sales[Unit Price] )
Margin         = [Total Sales] - [Total Cost]
Margin %       = DIVIDE ( [Margin], [Total Sales] )
'''),
        TABLE([("Function", "函数"), ("Counts / returns", "计算 / 返回")], [
            [("<code>SUM</code>, <code>AVERAGE</code>, <code>MIN</code>, <code>MAX</code>", "<code>SUM</code>、<code>AVERAGE</code>、<code>MIN</code>、<code>MAX</code>"), ("The usual aggregations of one column", "单列的常用聚合")],
            [("<code>COUNT</code>", "<code>COUNT</code>"), ("Non-blank values in a column", "列中的非空值数量")],
            [("<code>COUNTA</code>", "<code>COUNTA</code>"), ("Non-blank values of any type", "任何类型的非空值数量")],
            [("<code>COUNTBLANK</code>", "<code>COUNTBLANK</code>"), ("Blank values", "空值数量")],
            [("<code>COUNTROWS</code>", "<code>COUNTROWS</code>"), ("Rows in a table (after filters)", "表的行数（经筛选后）")],
            [("<code>DISTINCTCOUNT</code>", "<code>DISTINCTCOUNT</code>"), ("Different values in a column", "列中不同值的数量")],
            [("<code>DIVIDE(a, b)</code>", "<code>DIVIDE(a, b)</code>"), ("a / b, returning BLANK (or a value you give) instead of an error when b is 0", "a / b；当 b 为 0 时返回 BLANK（或你指定的值），而不是错误")],
        ]),
        H("Basic statistical functions", "基本统计函数"),
        P("The exam lists \"basic statistical functions\": <code>AVERAGE</code>, <code>MEDIAN</code>, <code>MIN</code>/<code>MAX</code>, <code>STDEV.S</code>/<code>STDEV.P</code> (sample vs population standard deviation), <code>VAR.S</code>/<code>VAR.P</code>, <code>PERCENTILE.INC</code>, and <code>RANKX</code> for ranking. Their X versions (AVERAGEX, MEDIANX…) iterate over a table first.",
          "考试列出了「基本统计函数」：<code>AVERAGE</code>、<code>MEDIAN</code>、<code>MIN</code>/<code>MAX</code>、<code>STDEV.S</code>/<code>STDEV.P</code>（样本与总体标准差）、<code>VAR.S</code>/<code>VAR.P</code>、<code>PERCENTILE.INC</code>，以及用于排名的 <code>RANKX</code>。它们的 X 版本（AVERAGEX、MEDIANX……）会先遍历一张表。"),
        Q("Sales has one row per order line. Which measure counts the number of orders?",
          "Sales 表每个订单明细一行。哪个度量值能计算订单数量？",
          O(True, "DISTINCTCOUNT(Sales[OrderID])", "DISTINCTCOUNT(Sales[OrderID])", "Right: each order appears on several lines.", "对：每个订单会出现在多行明细中。"),
          O(False, "COUNTROWS(Sales)", "COUNTROWS(Sales)", "That counts order lines.", "这计算的是订单明细行数。"),
          O(False, "COUNT(Sales[OrderID])", "COUNT(Sales[OrderID])", "COUNT counts every non-blank line, duplicates included.", "COUNT 会计算每一个非空行，包括重复的。"),
          O(False, "SUM(Sales[OrderID])", "SUM(Sales[OrderID])", "", "")),
        Q("Why use DIVIDE([A], [B]) instead of [A] / [B]?",
          "为什么用 DIVIDE([A], [B]) 而不是 [A] / [B]？",
          O(True, "It handles division by zero safely, returning BLANK or an alternate result", "它能安全地处理除以零，返回 BLANK 或替代结果", "", ""),
          O(False, "It is required for percentages", "百分比必须用它", "", ""),
          O(False, "It rounds the result", "它会四舍五入结果", "", ""),
          O(False, "It ignores filters", "它会忽略筛选", "", "")),
    ], terms=["measure", "implicit-measure"], url=DAX + "dax-overview"),

    lesson("context", ("Row context and filter context", "行上下文与筛选上下文"), 9, [
        ("Filter context is the set of filters on a calculation: slicers, visual axes, filters and RLS.",
         "筛选上下文是计算所受的筛选条件：切片器、视觉对象的轴、筛选器和 RLS。"),
        ("Row context is \"the current row\", which exists in calculated columns and in iterators such as SUMX.",
         "行上下文是「当前行」，存在于计算列和 SUMX 等迭代器中。"),
        ("Row context does not filter by itself; CALCULATE (or calling a measure) turns it into filter context — context transition.",
         "行上下文本身不会筛选；CALCULATE（或调用度量值）会把它变成筛选上下文——这叫上下文转换。"),
    ], [
        P("Every DAX result depends on its <b>evaluation context</b>. Understanding the two kinds of context is the key to reading any DAX formula.",
          "每个 DAX 结果都取决于它的<b>计算上下文</b>。理解两种上下文，是读懂任何 DAX 公式的关键。"),
        TABLE([("", ""), ("Filter context", "筛选上下文"), ("Row context", "行上下文")], [
            [("Comes from", "来源"), ("Visual rows/columns, slicers, filter pane, cross-filtering, RLS, CALCULATE", "视觉对象的行/列、切片器、筛选器窗格、交叉筛选、RLS、CALCULATE"), ("Calculated columns; iterators (SUMX, FILTER, ADDCOLUMNS…)", "计算列；迭代器（SUMX、FILTER、ADDCOLUMNS……）")],
            [("Means", "含义"), ("Which rows of each table are visible", "每张表中哪些行可见"), ("Which single row is being evaluated", "正在计算的是哪一行")],
            [("Filters other tables?", "会筛选其他表吗？"), ("Yes, along relationships", "会，沿着关系传递"), ("No — use RELATED to read the one side", "不会——用 RELATED 读取「一」端的值")],
        ]),
        P("Example: in a matrix with Product[Category] on rows, the cell for \"Bikes\" evaluates <code>[Total Sales]</code> with the filter context Category = Bikes. The same measure in the total row has no Category filter.",
          "例子：在行是 Product[Category] 的矩阵中，「Bikes」单元格以筛选上下文 Category = Bikes 计算 <code>[Total Sales]</code>。同一个度量值在总计行就没有 Category 筛选。"),
        H("Context transition", "上下文转换"),
        P("In a calculated column on Customer, <code>SUM(Sales[Amount])</code> returns the grand total on every row: the row context of Customer does not filter Sales. Wrapping it in CALCULATE, or referencing a measure (which has an implicit CALCULATE), converts the current row into a filter: now each customer gets their own sales.",
          "在 Customer 表的计算列中，<code>SUM(Sales[Amount])</code> 在每一行都返回总计：Customer 的行上下文不会筛选 Sales。用 CALCULATE 包起来，或引用一个度量值（度量值自带隐式 CALCULATE），就会把当前行转换成筛选：这样每个客户都得到自己的销售额。"),
        CODE('''
-- Calculated columns on the Customer table
Wrong     = SUM ( Sales[Amount] )                  -- same grand total on every row
Right     = CALCULATE ( SUM ( Sales[Amount] ) )    -- this customer's sales
Also Right = [Total Sales]                          -- a measure triggers context transition
'''),
        Q("A calculated column on Customer uses SUM(Sales[Amount]) and shows the same value on every row. Why?",
          "Customer 表上的计算列使用 SUM(Sales[Amount])，每一行都显示相同的值。为什么？",
          O(True, "Row context does not filter related tables without context transition", "没有上下文转换时，行上下文不会筛选相关的表", "Right: wrap it in CALCULATE or use a measure.", "对：用 CALCULATE 包起来，或改用度量值。"),
          O(False, "The relationship is inactive", "关系是非活动的", "", ""),
          O(False, "SUM only works in measures", "SUM 只能用在度量值中", "", ""),
          O(False, "The column needs a data category", "该列需要数据类别", "", "")),
    ], terms=["filter-context", "row-context", "context-transition"], url=DAX + "dax-overview#context"),

    lesson("calculate", ("The CALCULATE function", "CALCULATE 函数"), 10, [
        ("CALCULATE(expression, filters…) evaluates an expression in a modified filter context.",
         "CALCULATE(表达式, 筛选条件…) 在修改后的筛选上下文中计算表达式。"),
        ("A filter argument on a column replaces the existing filter on that column; KEEPFILTERS intersects instead.",
         "对某列的筛选参数会取代该列现有的筛选；KEEPFILTERS 则改为取交集。"),
        ("ALL / REMOVEFILTERS remove filters (for % of total); ALLEXCEPT keeps only some; ALLSELECTED respects the user's selections.",
         "ALL / REMOVEFILTERS 移除筛选（用于占总计百分比）；ALLEXCEPT 只保留部分筛选；ALLSELECTED 会尊重用户的选择。"),
    ], [
        P("<b>CALCULATE</b> is the most important function in DAX. It is the only way (with CALCULATETABLE) to change the filter context of a calculation.",
          "<b>CALCULATE</b> 是 DAX 中最重要的函数。它（以及 CALCULATETABLE）是改变计算的筛选上下文的唯一方法。"),
        CODE('''
Red Sales        = CALCULATE ( [Total Sales], Product[Colour] = "Red" )
Red Sales (kept) = CALCULATE ( [Total Sales], KEEPFILTERS ( Product[Colour] = "Red" ) )
All Sales        = CALCULATE ( [Total Sales], REMOVEFILTERS ( Product ) )
% of All Products = DIVIDE ( [Total Sales], [All Sales] )
% of Category    = DIVIDE ( [Total Sales],
                       CALCULATE ( [Total Sales], ALLEXCEPT ( Product, Product[Category] ) ) )
% of Selection   = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALLSELECTED ( Product ) ) )
Big Orders       = CALCULATE ( [Total Sales], FILTER ( Sales, Sales[Amount] > 1000 ) )
'''),
        TABLE([("Modifier", "修饰函数"), ("Effect inside CALCULATE", "在 CALCULATE 中的作用")], [
            [("<code>Table[Col] = value</code>", "<code>Table[Col] = value</code>"), ("Replace any filter on that column with this one", "以此筛选取代该列上的任何筛选")],
            [("<code>KEEPFILTERS(…)</code>", "<code>KEEPFILTERS(…)</code>"), ("Add the filter on top of existing ones (intersection)", "在现有筛选之上再加这个筛选（交集）")],
            [("<code>ALL(Table or Column)</code> / <code>REMOVEFILTERS(…)</code>", "<code>ALL(表或列)</code> / <code>REMOVEFILTERS(…)</code>"), ("Remove filters — the grand total denominator", "移除筛选——总计的分母")],
            [("<code>ALLEXCEPT(Table, Col…)</code>", "<code>ALLEXCEPT(表, 列…)</code>"), ("Remove all filters on the table except the listed columns", "移除表上所有筛选，只保留列出的列")],
            [("<code>ALLSELECTED(…)</code>", "<code>ALLSELECTED(…)</code>"), ("Remove filters from the visual but keep slicer and filter-pane selections", "移除视觉对象内的筛选，但保留切片器和筛选器窗格的选择")],
            [("<code>USERELATIONSHIP(a, b)</code>", "<code>USERELATIONSHIP(a, b)</code>"), ("Use an inactive relationship", "使用非活动关系")],
            [("<code>CROSSFILTER(a, b, dir)</code>", "<code>CROSSFILTER(a, b, 方向)</code>"), ("Change filter direction for this calculation", "为这个计算改变筛选方向")],
            [("<code>FILTER(Table, condition)</code>", "<code>FILTER(表, 条件)</code>"), ("Row-by-row filter; needed for conditions on measures or several columns", "逐行筛选；条件涉及度量值或多个列时需要")],
        ]),
        EXAM("\"% of grand total that does not change when a user selects a slicer\" → ALL/REMOVEFILTERS. \"% of the total of what the user selected\" → ALLSELECTED.",
             "「不随用户选择切片器而改变的总计百分比」→ ALL/REMOVEFILTERS。「占用户所选范围合计的百分比」→ ALLSELECTED。"),
        Q("In a matrix by Product, you need each product's share of sales across all products. Which denominator is right?",
          "在按 Product 分行的矩阵中，你需要每个产品占所有产品销售额的比例。哪个分母正确？",
          O(True, "CALCULATE([Total Sales], REMOVEFILTERS(Product))", "CALCULATE([Total Sales], REMOVEFILTERS(Product))", "Right: the product filter from the row is removed.", "对：移除了来自行的产品筛选。"),
          O(False, "CALCULATE([Total Sales], Product[Name] = \"All\")", "CALCULATE([Total Sales], Product[Name] = \"All\")", "", ""),
          O(False, "SUM(Sales[Amount])", "SUM(Sales[Amount])", "That still respects the row's product filter.", "这仍然受行的产品筛选影响。"),
          O(False, "SUMX(Product, [Total Sales])", "SUMX(Product, [Total Sales])", "Still evaluated within the row's product filter.", "仍在行的产品筛选范围内计算。")),
        Q("A matrix has Colour on rows. Measure: CALCULATE([Total Sales], Product[Colour] = \"Red\"). What does the Blue row show?",
          "矩阵的行是 Colour。度量值：CALCULATE([Total Sales], Product[Colour] = \"Red\")。Blue 那一行显示什么？",
          O(True, "Red sales — the filter argument replaces the row's Colour filter", "红色的销售额——筛选参数取代了行的 Colour 筛选", "Right: use KEEPFILTERS to get blank for non-red rows.", "对：若要让非红色行显示空白，使用 KEEPFILTERS。"),
          O(False, "Blank", "空白", "That is the KEEPFILTERS behaviour.", "那是 KEEPFILTERS 的行为。"),
          O(False, "Blue sales", "蓝色的销售额", "", ""),
          O(False, "An error", "错误", "", "")),
    ], terms=["calculate", "filter-context", "allselected"], url=DAX + "calculate-function-dax"),

    lesson("iterators", ("Iterators, variables and handy functions", "迭代器、变量和常用函数"), 9, [
        ("Iterators (SUMX, AVERAGEX, MAXX, RANKX, FILTER) evaluate an expression row by row over a table, then aggregate.",
         "迭代器（SUMX、AVERAGEX、MAXX、RANKX、FILTER）逐行遍历一张表计算表达式，然后再聚合。"),
        ("Variables (VAR … RETURN) make measures readable and avoid calculating the same thing twice.",
         "变量（VAR … RETURN）让度量值更易读，并避免重复计算同一个东西。"),
        ("SELECTEDVALUE, HASONEVALUE, SWITCH(TRUE()) and BLANK handling are everyday tools.",
         "SELECTEDVALUE、HASONEVALUE、SWITCH(TRUE()) 和 BLANK 处理是日常工具。"),
    ], [
        P("SUM can only add up a column. When you need to multiply first and add after — quantity × price on each line — use an iterator.",
          "SUM 只能加总一列。当你需要先相乘再相加——每一行的数量 × 单价——就要用迭代器。"),
        CODE('''
Revenue = SUMX ( Sales, Sales[Quantity] * Sales[Unit Price] )

Avg Sales per Customer = AVERAGEX ( VALUES ( Customer[CustomerID] ), [Total Sales] )

Product Rank = RANKX ( ALL ( Product[Name] ), [Total Sales], , DESC, DENSE )

Sales vs Target % =
VAR Actual = [Total Sales]
VAR Target = [Sales Target]
RETURN
    IF ( NOT ISBLANK ( Target ), DIVIDE ( Actual - Target, Target ) )

Selected Region = SELECTEDVALUE ( Store[Region], "Several regions" )

Size Band =
SWITCH ( TRUE (),
    [Total Sales] >= 1000000, "Large",
    [Total Sales] >= 100000,  "Medium",
    "Small" )
'''),
        TABLE([("Function", "函数"), ("Use", "用途")], [
            [("<code>SUMX / AVERAGEX / MINX / MAXX / COUNTX</code>", "<code>SUMX / AVERAGEX / MINX / MAXX / COUNTX</code>"), ("Row-by-row expression, then aggregate", "逐行计算表达式，再聚合")],
            [("<code>RANKX(table, expr)</code>", "<code>RANKX(表, 表达式)</code>"), ("Rank of the current item; use ALL() so it ranks against every item", "当前项目的排名；用 ALL() 才会与所有项目比较")],
            [("<code>VAR … RETURN</code>", "<code>VAR … RETURN</code>"), ("Store an intermediate result; evaluated once in the context where it is defined", "保存中间结果；在定义处的上下文中只计算一次")],
            [("<code>SELECTEDVALUE(col, alt)</code>", "<code>SELECTEDVALUE(列, 替代值)</code>"), ("The single selected value, or alt if zero or several", "唯一选中的值；若没有或有多个则返回替代值")],
            [("<code>HASONEVALUE(col)</code>", "<code>HASONEVALUE(列)</code>"), ("TRUE when exactly one value is in context — hide totals with it", "上下文中恰好只有一个值时为 TRUE——可用来隐藏总计")],
            [("<code>RELATED(col)</code>", "<code>RELATED(列)</code>"), ("From the many side, read a column on the one side (row context)", "在「多」端读取「一」端的列（行上下文）")],
            [("<code>SWITCH(TRUE(), …)</code>", "<code>SWITCH(TRUE(), …)</code>"), ("Readable multi-branch IF", "易读的多分支 IF")],
        ]),
        Q("Sales has Quantity and Unit Price but no amount column. Which measure gives total revenue correctly?",
          "Sales 有 Quantity 和 Unit Price，但没有金额列。哪个度量值能正确算出总收入？",
          O(True, "SUMX(Sales, Sales[Quantity] * Sales[Unit Price])", "SUMX(Sales, Sales[Quantity] * Sales[Unit Price])", "Right: multiply on each row, then sum.", "对：每行先相乘，再加总。"),
          O(False, "SUM(Sales[Quantity]) * SUM(Sales[Unit Price])", "SUM(Sales[Quantity]) * SUM(Sales[Unit Price])", "Multiplying two totals is not the sum of the products.", "两个合计相乘并不等于各行乘积的总和。"),
          O(False, "SUM(Sales[Quantity] * Sales[Unit Price])", "SUM(Sales[Quantity] * Sales[Unit Price])", "SUM accepts only a column.", "SUM 只接受一个列。"),
          O(False, "AVERAGE(Sales[Unit Price]) * COUNTROWS(Sales)", "AVERAGE(Sales[Unit Price]) * COUNTROWS(Sales)", "", "")),
        Q("A card must show the selected region's name, or \"All regions\" when none or several are selected. Which function?",
          "卡片要显示所选区域的名称；没选或选了多个时显示「All regions」。用哪个函数？",
          O(True, "SELECTEDVALUE(Store[Region], \"All regions\")", "SELECTEDVALUE(Store[Region], \"All regions\")", "", ""),
          O(False, "VALUES(Store[Region])", "VALUES(Store[Region])", "Returns a table; errors if more than one value in a card.", "返回的是表；在卡片中有多个值时会出错。"),
          O(False, "RELATED(Store[Region])", "RELATED(Store[Region])", "", ""),
          O(False, "FIRSTNONBLANK(Store[Region], 1)", "FIRSTNONBLANK(Store[Region], 1)", "Returns a value even when several are selected.", "即使选了多个，也会返回一个值。")),
    ], terms=["iterator", "variable", "context-transition"], url=DAX + "best-practices/dax-variables"),
], url=DAX + "dax-overview")

c08 = module("c08", ("Time intelligence and advanced DAX", "时间智能与进阶 DAX"), [
    lesson("time-intelligence", ("Time intelligence measures", "时间智能度量值"), 10, [
        ("Time intelligence functions shift or extend the dates in the filter context: year-to-date, same period last year, rolling periods.",
         "时间智能函数会移动或扩展筛选上下文中的日期：年初至今、去年同期、滚动期间。"),
        ("They need a marked date table with contiguous dates, and work through CALCULATE.",
         "它们需要一张已标记、日期连续的日期表，并通过 CALCULATE 运作。"),
        ("TOTALYTD and DATESYTD accept a fiscal year-end such as \"6/30\".",
         "TOTALYTD 和 DATESYTD 可以接受财年结束日，例如 \"6/30\"。"),
    ], [
        CODE('''
Sales YTD      = TOTALYTD ( [Total Sales], 'Date'[Date] )
Sales FYTD     = TOTALYTD ( [Total Sales], 'Date'[Date], "6/30" )   -- fiscal year ends 30 June
Sales MTD      = TOTALMTD ( [Total Sales], 'Date'[Date] )
Sales PY       = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
Sales PM       = CALCULATE ( [Total Sales], DATEADD ( 'Date'[Date], -1, MONTH ) )
YoY %          = DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )
Sales Last 3M  = CALCULATE ( [Total Sales],
                    DATESINPERIOD ( 'Date'[Date], MAX ( 'Date'[Date] ), -3, MONTH ) )
'''),
        TABLE([("Function", "函数"), ("Returns the dates of…", "返回哪些日期")], [
            [("<code>DATESYTD / TOTALYTD</code>", "<code>DATESYTD / TOTALYTD</code>"), ("Start of the year to the last date in context", "年初到上下文中的最后日期")],
            [("<code>DATESMTD, DATESQTD</code>", "<code>DATESMTD、DATESQTD</code>"), ("Month- or quarter-to-date", "月初或季初至今")],
            [("<code>SAMEPERIODLASTYEAR</code>", "<code>SAMEPERIODLASTYEAR</code>"), ("The same dates one year back", "往回推一年的相同日期")],
            [("<code>DATEADD(dates, n, interval)</code>", "<code>DATEADD(日期, n, 间隔)</code>"), ("Dates shifted by n days, months, quarters or years", "移动 n 天、月、季或年后的日期")],
            [("<code>PARALLELPERIOD</code>", "<code>PARALLELPERIOD</code>"), ("The whole parallel month/quarter/year (full period, not partial)", "整个对应的月/季/年（完整期间，而非部分）")],
            [("<code>DATESINPERIOD(dates, end, n, interval)</code>", "<code>DATESINPERIOD(日期, 结束日, n, 间隔)</code>"), ("A rolling window ending on a date", "以某日为结束的滚动窗口")],
            [("<code>PREVIOUSMONTH / NEXTYEAR …</code>", "<code>PREVIOUSMONTH / NEXTYEAR …</code>"), ("The whole previous/next period", "整个上一个/下一个期间")],
        ]),
        NOTE("caution", "Use the Date table's date column in these functions, not Sales[OrderDate]. The filter must come from the date table so that all fact tables shift together.",
             "这些函数要使用日期表的日期列，而不是 Sales[OrderDate]。筛选必须来自日期表，所有事实表才会一起移动。"),
        Q("Your fiscal year ends on 30 June. Which measure gives fiscal year-to-date sales?",
          "你的财年在 6 月 30 日结束。哪个度量值能算出财年至今的销售额？",
          O(True, "TOTALYTD([Total Sales], 'Date'[Date], \"6/30\")", "TOTALYTD([Total Sales], 'Date'[Date], \"6/30\")", "Right: the third argument sets the year-end date.", "对：第三个参数设定年度结束日。"),
          O(False, "TOTALYTD([Total Sales], 'Date'[Date])", "TOTALYTD([Total Sales], 'Date'[Date])", "That uses a 31 December year-end.", "这使用 12 月 31 日作为年度结束日。"),
          O(False, "CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))", "CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))", "", ""),
          O(False, "TOTALMTD([Total Sales], 'Date'[Date])", "TOTALMTD([Total Sales], 'Date'[Date])", "", "")),
        Q("Which expression returns sales for the 12 months ending on the last date in the current filter context?",
          "哪个表达式返回截至当前筛选上下文最后日期的 12 个月销售额？",
          O(True, "CALCULATE([Total Sales], DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH))", "CALCULATE([Total Sales], DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH))", "", ""),
          O(False, "CALCULATE([Total Sales], PARALLELPERIOD('Date'[Date], -12, MONTH))", "CALCULATE([Total Sales], PARALLELPERIOD('Date'[Date], -12, MONTH))", "That shifts back 12 months instead of covering them.", "这是往回移 12 个月，而不是涵盖 12 个月。"),
          O(False, "TOTALYTD([Total Sales], 'Date'[Date])", "TOTALYTD([Total Sales], 'Date'[Date])", "", ""),
          O(False, "CALCULATE([Total Sales], PREVIOUSYEAR('Date'[Date]))", "CALCULATE([Total Sales], PREVIOUSYEAR('Date'[Date]))", "", "")),
    ], terms=["time-intelligence", "date-table"], url=DAX + "time-intelligence-functions-dax"),

    lesson("semi-additive", ("Semi-additive measures", "半累加度量值"), 7, [
        ("Balances and stock levels can be added across products or accounts, but not across time.",
         "余额和库存可以跨产品或账户相加，但不能跨时间相加。"),
        ("Return the value on the last date of the period: LASTDATE, LASTNONBLANK or CLOSINGBALANCEMONTH/QUARTER/YEAR.",
         "返回期间最后一天的值：LASTDATE、LASTNONBLANK 或 CLOSINGBALANCEMONTH/QUARTER/YEAR。"),
        ("Use LASTNONBLANK when the last calendar date may have no snapshot.",
         "当日历的最后一天可能没有快照数据时，用 LASTNONBLANK。"),
    ], [
        P("A warehouse counts 100 bikes on 31 January and 120 on 28 February. The stock for \"Q1 so far\" is 120, not 220. Measures like this are <b>semi-additive</b>: they sum across some dimensions (warehouses, products) but not across dates.",
          "某仓库 1 月 31 日盘点有 100 辆自行车，2 月 28 日有 120 辆。「第一季度至今」的库存是 120，而不是 220。这类度量值是<b>半累加</b>的：可以跨某些维度（仓库、产品）加总，但不能跨日期加总。"),
        CODE('''
Stock on Hand =
CALCULATE ( SUM ( Inventory[Units] ), LASTDATE ( 'Date'[Date] ) )

Stock (last snapshot) =
CALCULATE (
    SUM ( Inventory[Units] ),
    LASTNONBLANK ( 'Date'[Date], CALCULATE ( SUM ( Inventory[Units] ) ) )
)

Month-end Balance = CLOSINGBALANCEMONTH ( SUM ( Account[Balance] ), 'Date'[Date] )
Opening Balance   = OPENINGBALANCEMONTH ( SUM ( Account[Balance] ), 'Date'[Date] )
Average Stock     = AVERAGEX ( VALUES ( 'Date'[Date] ), [Stock on Hand] )
'''),
        P("<code>LASTDATE</code> takes the last date of the period in the date table. If snapshots exist only on business days, the last date (a Sunday, say) has no data and the result is blank — <code>LASTNONBLANK</code> finds the last date that actually has a value.",
          "<code>LASTDATE</code> 取日期表中该期间的最后一天。如果快照只在工作日才有，最后一天（例如星期日）就没有数据，结果为空——<code>LASTNONBLANK</code> 会找出真正有值的最后一天。"),
        Q("Inventory is captured on weekdays only. A monthly stock measure using LASTDATE shows blanks for some months. What fixes it?",
          "库存只在工作日记录。使用 LASTDATE 的月库存度量值在某些月份显示空白。怎么修正？",
          O(True, "Use LASTNONBLANK over the dates", "对日期使用 LASTNONBLANK", "Right: months that end on a weekend have no row on the last date.", "对：以周末结束的月份，最后一天没有数据行。"),
          O(False, "Use SUM without CALCULATE", "直接用 SUM，不用 CALCULATE", "That adds up every day's stock.", "这会把每天的库存加总。"),
          O(False, "Use TOTALYTD", "用 TOTALYTD", "", ""),
          O(False, "Turn on Auto date/time", "开启「自动日期/时间」", "", "")),
    ], terms=["semi-additive"], url=DAX + "closingbalancemonth-function-dax"),

    lesson("quick-measures", ("Quick measures", "快速度量值"), 5, [
        ("Quick measures generate DAX from a dialog: running total, year-over-year change, weighted average, filtered values and more.",
         "快速度量值通过对话框生成 DAX：累计总计、同比变化、加权平均、筛选后的值等。"),
        ("The result is an ordinary measure you can read, rename and edit.",
         "结果是一个普通的度量值，可以阅读、重命名和编辑。"),
        ("Time-based quick measures need a date table or the Auto date hierarchy.",
         "基于时间的快速度量值需要日期表或自动日期层次结构。"),
    ], [
        P("Right-click a table in the Data pane and choose <b>New quick measure</b>. Pick a calculation, drop fields into the slots, and Power BI writes the DAX. In current versions you can also describe the measure in words and let Copilot suggest the DAX, if Copilot is enabled for your tenant.",
          "在「数据」窗格中右键单击一张表，选择<b>新建快速度量值</b>。选择计算类型，把字段拖进对应位置，Power BI 就会写出 DAX。在新版本中，如果租户启用了 Copilot，也可以用文字描述度量值，让 Copilot 建议 DAX。"),
        TABLE([("Category", "类别"), ("Examples", "例子")], [
            [("Aggregate per category", "按类别聚合"), ("Average per category, variance, max/min per category, weighted average", "按类别的平均值、方差、最大/最小值、加权平均")],
            [("Filters", "筛选器"), ("Filtered value, difference from filtered value, % difference, sales from new customers", "筛选后的值、与筛选值的差、百分比差异、新客户的销售额")],
            [("Time intelligence", "时间智能"), ("Year-to-date total, quarter-to-date, month-to-date, year-over-year change, rolling average", "年初至今总计、季初至今、月初至今、同比变化、滚动平均")],
            [("Totals", "总计"), ("Running total, total for category (filters applied or not)", "累计总计、类别总计（是否套用筛选）")],
            [("Mathematical operations", "数学运算"), ("Addition, subtraction, multiplication, division, percentage difference, correlation coefficient", "加、减、乘、除、百分比差异、相关系数")],
            [("Text", "文本"), ("Star rating, concatenated list of values", "星级评分、串接的值列表")],
        ]),
        Q("A business user who does not know DAX needs a running total of sales by date. What is the quickest correct approach?",
          "一位不懂 DAX 的业务用户需要按日期计算销售额的累计总计。最快的正确方法是什么？",
          O(True, "New quick measure → Running total", "新建快速度量值 → 累计总计", "Right: it generates the DAX for you.", "对：它会为你生成 DAX。"),
          O(False, "Add a calculated column with SUM", "新增使用 SUM 的计算列", "", ""),
          O(False, "Use the Analytics pane", "使用「分析」窗格", "The Analytics pane adds reference lines, not running totals.", "「分析」窗格加的是参考线，不是累计总计。"),
          O(False, "Group By in Power Query", "在 Power Query 中分组", "", "")),
    ], terms=["quick-measure"], url=PBI + "transform-model/desktop-quick-measures"),

    lesson("calculation-groups", ("Calculation groups", "计算组"), 8, [
        ("A calculation group applies the same logic (YTD, PY, YoY %) to any measure, so you do not write it for every measure.",
         "计算组把同一套逻辑（年初至今、去年、同比 %）套用到任何度量值，不必为每个度量值重写。"),
        ("Each calculation item uses SELECTEDMEASURE() as a placeholder for the measure in the visual.",
         "每个计算项用 SELECTEDMEASURE() 代表视觉对象中的度量值。"),
        ("Creating a calculation group turns on \"discourage implicit measures\": only explicit measures work with it.",
         "建立计算组会开启「不鼓励隐式度量值」：只有显式度量值才能配合使用。"),
    ], [
        P("Ten base measures × five time variations = fifty measures to write and maintain. A <b>calculation group</b> collapses that to ten measures plus one group with five <b>calculation items</b>. Put the group's column in a slicer or on matrix columns and every measure gets the variations.",
          "10 个基础度量值 × 5 种时间变化 = 要编写和维护 50 个度量值。<b>计算组</b>可以把它简化为 10 个度量值加上一个包含 5 个<b>计算项</b>的组。把计算组的列放进切片器或矩阵的列中，每个度量值都会得到这些变化。"),
        CODE('''
-- Calculation group "Time Calc", column "Period"
Current = SELECTEDMEASURE ()
YTD     = CALCULATE ( SELECTEDMEASURE (), DATESYTD ( 'Date'[Date] ) )
PY      = CALCULATE ( SELECTEDMEASURE (), SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
YoY %   =
    VAR Cur = SELECTEDMEASURE ()
    VAR Prev = CALCULATE ( SELECTEDMEASURE (), SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
    RETURN DIVIDE ( Cur - Prev, Prev )
'''),
        UL(("Create it in <b>Model view → Calculation group</b> in Power BI Desktop (or with Tabular Editor).",
            "在 Power BI Desktop 的<b>模型视图 → 计算组</b>中建立（或使用 Tabular Editor）。"),
           ("A <b>format string expression</b> per item can show YoY % as a percentage while the others stay currency.",
            "每个项目的<b>格式字符串表达式</b>可以让「同比 %」显示为百分比，其他项目仍保持货币格式。"),
           ("<b>Precedence</b> decides the order when two calculation groups apply to the same measure.",
            "当两个计算组作用于同一个度量值时，<b>优先级</b>决定先后顺序。")),
        Q("You have 12 base measures and need YTD, PY and YoY % for each. What minimises the number of measures to maintain?",
          "你有 12 个基础度量值，每个都需要年初至今、去年和同比 %。怎样能让需要维护的度量值最少？",
          O(True, "A calculation group with YTD, PY and YoY % items", "一个包含 YTD、PY 和 YoY % 项目的计算组", "Right: 12 measures plus one group instead of 48 measures.", "对：只需 12 个度量值加一个组，而不是 48 个度量值。"),
          O(False, "Quick measures for each", "为每个都建立快速度量值", "Still 36 extra measures.", "仍然要多出 36 个度量值。"),
          O(False, "Calculated columns", "计算列", "", ""),
          O(False, "Field parameters", "字段参数", "Field parameters let users switch fields, not apply time logic.", "字段参数让用户切换字段，而不是套用时间逻辑。")),
        Q("Inside a calculation item, which function stands for the measure currently in the visual?",
          "在计算项中，哪个函数代表视觉对象中当前的度量值？",
          O(True, "SELECTEDMEASURE()", "SELECTEDMEASURE()", "", ""),
          O(False, "SELECTEDVALUE()", "SELECTEDVALUE()", "That returns a column value.", "它返回的是列值。"),
          O(False, "ISINSCOPE()", "ISINSCOPE()", "", ""),
          O(False, "CURRENTGROUP()", "CURRENTGROUP()", "", "")),
    ], terms=["calculation-group", "implicit-measure"], url=PBI + "transform-model/calculation-groups"),
], url=DAX + "time-intelligence-functions-dax")

c09 = module("c09", ("Optimize model performance", "优化模型性能"), [
    lesson("remove", ("Remove what you do not need", "删除不需要的内容"), 7, [
        ("Every column and row costs memory and refresh time; remove columns no report uses and rows outside the needed period.",
         "每个列和每一行都消耗内存和刷新时间；删除没有报表使用的列，以及所需期间以外的行。"),
        ("High-cardinality columns (GUIDs, timestamps, free text, many decimals) compress worst — remove, split or round them.",
         "高基数的列（GUID、时间戳、自由文本、很多位小数）压缩效果最差——要删除、拆分或四舍五入。"),
        ("Turn off Auto date/time and prefer integer keys.",
         "关闭「自动日期/时间」，优先使用整数键。"),
    ], [
        P("Import models are compressed column by column. A column with few distinct values (Country) compresses to almost nothing; a column where every value is different (TransactionGUID, a Date/Time to the second) barely compresses at all. The fastest model is a small one.",
          "导入模型是按列压缩的。非重复值很少的列（国家/地区）几乎不占空间；每个值都不同的列（TransactionGUID、精确到秒的日期/时间）几乎压缩不了。最快的模型就是小的模型。"),
        TABLE([("Action", "做法"), ("Why", "原因")], [
            [("Remove unused columns in Power Query", "在 Power Query 中删除没用的列"), ("Fewer columns = less memory, faster refresh", "列越少，内存越少、刷新越快")],
            [("Filter rows to the needed history (e.g. last 3 years)", "把行筛选到需要的历史范围（如最近 3 年）"), ("Fewer rows everywhere", "所有地方的行都会变少")],
            [("Split Date/Time into Date and Time; drop seconds", "把日期/时间拆成日期和时间；去掉秒"), ("Lower cardinality per column", "降低每列的基数")],
            [("Round or use Fixed decimal", "四舍五入或使用定点小数"), ("Fewer distinct values", "减少非重复值")],
            [("Integer surrogate keys instead of long text keys", "用整数代理键代替很长的文字键"), ("Smaller, faster relationships", "关系更小、更快")],
            [("Disable Auto date/time (Options → Data load)", "停用「自动日期/时间」（选项 → 数据加载）"), ("Removes hidden date tables for every date column", "移除每个日期列的隐藏日期表")],
            [("Replace calculated columns with Power Query columns", "用 Power Query 列代替计算列"), ("Better compression", "压缩更好")],
            [("Avoid bidirectional relationships unless needed", "非必要不用双向关系"), ("Simpler, faster filter propagation", "筛选传递更简单、更快")],
        ]),
        Q("Which column is likely to make an Import model much larger than necessary?",
          "哪个列最可能让导入模型变得远比需要的大？",
          O(True, "A unique transaction GUID that no report uses", "没有报表使用的唯一交易 GUID", "Right: every value is different and it adds nothing.", "对：每个值都不同，而且毫无用处。"),
          O(False, "Product category", "产品类别", "Low cardinality compresses well.", "低基数压缩效果很好。"),
          O(False, "A Date column used by the date relationship", "日期关系使用的日期列", "", ""),
          O(False, "A Year column", "年份列", "", "")),
    ], terms=["cardinality-column", "vertipaq", "auto-date-time"], url=PBI + "guidance/import-modeling-data-reduction"),

    lesson("performance-analyzer", ("Performance Analyzer and DAX query view", "性能分析器与 DAX 查询视图"), 8, [
        ("Performance Analyzer records, per visual, the time spent on the DAX query, visual display and other (waiting).",
         "性能分析器按视觉对象记录 DAX 查询、视觉对象显示和其他（等待）所花的时间。"),
        ("Copy a visual's query into DAX query view (or DAX Studio) to test and tune the measure.",
         "把视觉对象的查询复制到 DAX 查询视图（或 DAX Studio）中，测试和调整度量值。"),
        ("Slow DAX query → fix the measure or model; slow visual display → too many points or visuals on the page.",
         "DAX 查询慢 → 修正度量值或模型；视觉对象显示慢 → 数据点或页面上的视觉对象太多。"),
    ], [
        OL(("In Desktop open <b>Optimize → Performance analyzer</b> (or View → Performance analyzer).", "在 Desktop 中打开<b>优化 → 性能分析器</b>（或「视图 → 性能分析器」）。"),
           ("Select <b>Start recording</b>, then <b>Refresh visuals</b> or interact with the page.", "选择<b>开始录制</b>，然后<b>刷新视觉对象</b>或与页面互动。"),
           ("Expand each visual to see its timings, sorted by duration.", "展开每个视觉对象，查看按耗时排序的时间。"),
           ("<b>Copy query</b> and paste it into <b>DAX query view</b> to run it, change the measure and compare.", "<b>复制查询</b>，粘贴到 <b>DAX 查询视图</b>中执行、修改度量值并比较。")),
        TABLE([("Timing", "时间项目"), ("What it measures", "测量什么"), ("If it is large", "如果很大")], [
            [("DAX query", "DAX 查询"), ("Time for the engine to answer the query", "引擎回答查询的时间"), ("Simplify the measure (variables, avoid FILTER on whole tables), check relationships and model size", "简化度量值（用变量、避免对整张表 FILTER），检查关系和模型大小")],
            [("Visual display", "视觉对象显示"), ("Time to draw the visual", "绘制视觉对象的时间"), ("Fewer data points, simpler custom visuals", "减少数据点，使用较简单的自定义视觉对象")],
            [("Other", "其他"), ("Waiting for other visuals or background work", "等待其他视觉对象或后台工作"), ("Fewer visuals on the page; use drill-through or tooltips instead", "减少页面上的视觉对象；改用钻取或工具提示")],
        ]),
        P("<b>DAX query view</b> is a tab in Power BI Desktop where you write <code>EVALUATE</code> queries against the model. It can define measures temporarily in a <code>DEFINE</code> block, run them, and update the model with the improved version. Quick queries (right-click a table or measure) generate starter queries for you.",
          "<b>DAX 查询视图</b>是 Power BI Desktop 中的一个选项卡，可以对模型编写 <code>EVALUATE</code> 查询。你可以在 <code>DEFINE</code> 区块中临时定义度量值、执行它们，再把改进后的版本更新到模型。快速查询（右键单击表或度量值）会为你生成起始查询。"),
        CODE('''
DEFINE
    MEASURE Sales[Total Sales] = SUM ( Sales[Amount] )
EVALUATE
SUMMARIZECOLUMNS ( Product[Category], "Sales", [Total Sales] )
ORDER BY [Sales] DESC
'''),
        NOTE("key", "The <b>Optimize</b> ribbon also has <b>Pause visuals</b> (stop queries while you edit) and optimization presets that add an Apply button to slicers and filters, so each click does not send a new query.",
             "<b>优化</b>功能区还有<b>暂停视觉对象</b>（编辑时停止发送查询），以及优化预设：为切片器和筛选器加上「应用」按钮，避免每次点击都发送新查询。"),
        Q("Performance Analyzer shows a table visual with DAX query 120 ms, Visual display 4,800 ms. What is the most likely fix?",
          "性能分析器显示某个表格视觉对象：DAX 查询 120 毫秒、视觉对象显示 4,800 毫秒。最可能的解决方法是什么？",
          O(True, "Reduce the number of rows or data points the visual renders", "减少视觉对象要呈现的行数或数据点", "Right: the query is fast; drawing is slow.", "对：查询很快，绘制很慢。"),
          O(False, "Rewrite the measure", "重写度量值", "The DAX part is only 120 ms.", "DAX 部分只有 120 毫秒。"),
          O(False, "Switch the table to DirectQuery", "把表改为 DirectQuery", "That usually makes the query slower.", "那通常会让查询更慢。"),
          O(False, "Add a bidirectional relationship", "新增双向关系", "", "")),
        Q("Where can you run and tune the DAX query that a slow visual generates, without leaving Power BI Desktop?",
          "在不离开 Power BI Desktop 的情况下，可以在哪里执行和调整慢速视觉对象所生成的 DAX 查询？",
          O(True, "DAX query view", "DAX 查询视图", "", ""),
          O(False, "Power Query Editor", "Power Query 编辑器", "Power Query uses M, not DAX queries.", "Power Query 使用 M，不是 DAX 查询。"),
          O(False, "The Analytics pane", "「分析」窗格", "", ""),
          O(False, "Model view properties", "模型视图的属性", "", "")),
    ], terms=["performance-analyzer", "dax-query-view"], url=PBI + "create-reports/desktop-performance-analyzer"),

    lesson("granularity", ("Reduce granularity", "降低粒度"), 6, [
        ("Granularity is what one row of a fact table represents: a transaction, a day per product, a month per store.",
         "粒度是事实表中一行所代表的内容：一笔交易、每个产品每天、每家门店每月。"),
        ("If reports never need transaction detail, group the fact table to a coarser grain to cut rows dramatically.",
         "如果报表从不需要交易明细，就把事实表分组到较粗的粒度，可大幅减少行数。"),
        ("Keep detail available through DirectQuery or a separate detail table if a few users need it.",
         "如果少数用户需要明细，可以通过 DirectQuery 或另一张明细表提供。"),
    ], [
        P("Reducing <b>granularity</b> (summarising) is the biggest lever for model size. Fifty million sales lines grouped to one row per day, store and product might become two million rows — and every visual that shows daily or monthly figures gives the same answer.",
          "降低<b>粒度</b>（汇总）是缩小模型最有效的方法。五千万行的销售明细，按日、门店和产品分组后可能只剩两百万行——而所有显示每日或每月数据的视觉对象，答案都一样。"),
        UL(("Decide the grain from the questions the report must answer, not from what the source happens to hold.",
            "根据报表必须回答的问题来决定粒度，而不是根据数据源碰巧有什么。"),
           ("Group By in Power Query (or in the source view) to the chosen grain; sum the additive numbers, and keep a count if you need averages.",
            "在 Power Query（或数据源视图）中用「分组依据」整理到选定的粒度；对可加总的数字求和，若需要平均值就保留一个计数。"),
           ("A coarser fact table can still join the same dimensions, as long as it keeps their keys.",
            "较粗粒度的事实表只要保留维度表的键，仍可连接相同的维度表。"),
           ("For huge DirectQuery sources, <b>aggregations</b> keep a small imported summary table that answers most queries, falling back to the detail table only when needed.",
            "对于超大的 DirectQuery 数据源，<b>聚合</b>会保留一张小的导入汇总表来回答大多数查询，只在需要时才回到明细表。")),
        Q("Reports only ever show sales by day, product and store, but the model imports 80 million transaction rows. What reduces the model most?",
          "报表只会按日、产品和门店显示销售额，但模型导入了 8,000 万行交易数据。哪种做法最能缩小模型？",
          O(True, "Group the fact table by date, product and store in Power Query", "在 Power Query 中按日期、产品和门店对事实表分组", "Right: fewer rows, same answers.", "对：行更少，答案相同。"),
          O(False, "Change the cross-filter direction", "改变交叉筛选方向", "", ""),
          O(False, "Add more measures", "新增更多度量值", "", ""),
          O(False, "Mark the date table", "标记日期表", "", "")),
    ], terms=["granularity", "aggregations"], url=PBI + "guidance/import-modeling-data-reduction"),
], url=PBI + "guidance/power-bi-optimization")

MODULES = [c06, c07, c08, c09]
