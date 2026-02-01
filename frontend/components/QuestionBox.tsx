"use client"
import { useState } from "react"
import { askQuestion } from "@/lib/api"


const QuestionBox = (
  {onAnswer,} : {onAnswer : (ans : string, time : number) => void}
) => {

  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)

  async function submit(){
    if (!query) return;
    setLoading(true);

    const start = performance.now();
    const res = await askQuestion(query);
    const end = performance.now()

    onAnswer(res.answer, end - start);
    setLoading(false)
  }

  return (
    <div className="flex gap-2 mt-8">
      <input
        className="border bg-amber-900 border-red-900 text-[18px] p-4 w-170 flex-1 rounded-2xl"
        placeholder="Ask a question..."
        value = {query}
        onChange = {(e) => setQuery(e.target.value)}
      />
      <button
        onClick={submit}
        className="bg-red-700 shadow-2xl hover:bg-red-600 transition-all duration-300 text-white text-[20px] cursor-pointer font-semibold px-4 w-30 rounded-2xl"
      >
      {loading ? "Thinking.." : "Ask"}
      </button>
    </div>
  )
}

export default QuestionBox