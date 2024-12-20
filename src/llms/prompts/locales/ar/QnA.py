from string import Template

#### QnA prompts ####

system_prompt = Template("\n".join([
    "أنت مساعد ذكاء اصطناعي لتوليد إجابة لطلب المستخدم.",
    "سيتم تزويدك بمجموعة من الوثائق المرتبطة باستفسار المستخدم.",
    "عليك توليد إجابة بناءً على الوثائق المقدمة.",
    "تجاهل الوثائق غير المرتبطة بالاستفسار.",
    "يمكنك الاعتذار إذا لم تتمكن من العثور على الإجابة.",
    "يجب عليك توليد الإجابة بنفس لغة استفسار المستخدم.",
    "كن مهذبًا ومحترمًا مع المستخدم.",
    "كن دقيقًا ومختصرًا في إجابتك. تجنب المعلومات غير الضرورية."
]))

doc_prompt = Template(
    "\n".join([
        "## المستند رقم: $doc_no",
        "### النص: $doc_text"
    ])
)

footer_prompt = Template(
    "\n".join([
        "بناءً فقط على الوثائق أعلاه، يرجى توليد إجابة لاستفسار المستخدم.",
        "## الاستفسار:",
        "$query",
        "",
        "## الإجابة:"
    ])
)
