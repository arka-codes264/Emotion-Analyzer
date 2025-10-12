import { useState } from 'react'

function Home() {
  const [duration, setDuration] = useState(10)

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Home</h1>
        <p className="text-gray-600 mt-1">Select a duration and start detection.</p>
      </header>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="grid gap-6 md:grid-cols-3 items-end">
          <div className="md:col-span-2">
            <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-2">Duration</label>
            <select
              id="duration"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="w-full rounded-lg border-gray-300 focus:border-blue-600 focus:ring-blue-600"
            >
              <option value={10}>10 seconds</option>
              <option value={30}>30 seconds</option>
              <option value={60}>60 seconds</option>
            </select>
          </div>

          <button
            type="button"
            className="inline-flex items-center justify-center rounded-lg bg-blue-600 text-white px-6 py-3 font-medium hover:bg-blue-700 transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            onClick={() => {}}
          >
            Start Emotion Detection
          </button>
        </div>

        <div className="mt-8">
          <div className="h-64 rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 flex items-center justify-center text-gray-500">
            [Camera Feed Placeholder]
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
