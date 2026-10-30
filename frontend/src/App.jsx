
import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [query, setQuery] = useState('')
  const [source, setSource] = useState('wikipedia')
  const [limit, setLimit] = useState('20')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSearch(event) {
    event.preventDefault()

    if (!query.trim()) {
      setError('Please enter a search query.')
      return
    }

    setLoading(true)
    setError('')
    setResults([])

    try {
      const response = await fetch(
        `${API_URL}/search?query=${encodeURIComponent(query)}&source=${encodeURIComponent(source)}&limit=${limit}`
      )

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`)
      }

      const data = await response.json()

      setResults(data.results ?? [])

    } catch (err) {
      setError(
        'Could not retrieve results. Check that your backend is running and the endpoint exists.'
      )

      console.error(err)

    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="dashboard container-fluid py-4 px-3 px-md-5">

      {/* Header */}

      <header className="d-flex align-items-center gap-3 mb-5">

        <div className="brand-icon">
          <i className="bi bi-radar" />
        </div>

        <div>
          <h1 className="h3 mb-1">
            Web Intelligence
          </h1>

          <p className="text-secondary mb-0">
            Research, collect, and analyze information
          </p>
        </div>

      </header>

      {/* Search Section */}

      <section className="search-panel p-4 p-md-5 mb-4">

        <span className="section-label">
          RESEARCH WORKSPACE
        </span>

        <h2 className="h4 mt-3 mb-2">
          What do you want to explore?
        </h2>

        <p className="text-secondary mb-4">
          Search information and inspect the results returned by your sources.
        </p>

        <form onSubmit={handleSearch}>

          <div className="row g-2">

            {/* Search Input */}

            <div className="col-12 col-md">

              <input
                type="search"
                className="form-control form-control-lg"
                placeholder="Try renewable energy, machine learning..."
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                aria-label="Search query"
              />

            </div>

            {/* Source Selection */}

            <div className="col-12 col-md-3">

              <select
                className="form-select form-select-lg"
                value={source}
                onChange={(event) => setSource(event.target.value)}
                aria-label="Select source"
              >

                <option value="wikipedia">
                  Wikipedia
                </option>

                <option value="pokemon">
                  PokéAPI
                </option>

              </select>

            </div>

            {/* Article Limit */}

            <div className="col-12 col-md-2">

              <select
                className="form-select form-select-lg"
                value={limit}
                onChange={(event) => setLimit(event.target.value)}
                aria-label="Select number of results"
              >

                <option value="10">10 articles</option>
                <option value="20">20 articles</option>
                <option value="30">30 articles</option>
                <option value="50">50 articles</option>

              </select>

            </div>

            {/* Search Button */}

            <div className="col-12 col-md-auto">

              <button
                className="btn btn-primary btn-lg w-100"
                type="submit"
                disabled={loading}
              >

                {loading ? 'Searching...' : 'Search'}

              </button>

            </div>

          </div>

        </form>

      </section>

      {/* Statistics */}

      <section className="row g-3 mb-4">

        <div className="col-12 col-sm-6">

          <div className="stat-card p-4">

            <p className="text-secondary mb-2">
              Results retrieved
            </p>

            <div className="stat-value">
              {results.length}
            </div>

          </div>

        </div>

        <div className="col-12 col-sm-6">

          <div className="stat-card p-4">

            <p className="text-secondary mb-2">
              Selected source
            </p>

            <div className="stat-value text-capitalize">

              {source === 'pokemon' ? 'PokéAPI' : 'Wikipedia'}

            </div>

          </div>

        </div>

      </section>

      {/* Results Section */}

      <section>

        <div className="d-flex align-items-center justify-content-between mb-3">

          <h2 className="h5 mb-0">
            Search results
          </h2>

          <span className="text-secondary small">
            {results.length} items
          </span>

        </div>

        {/* Error Message */}

        {error && (

          <div
            className="alert alert-danger"
            role="alert"
          >

            {error}

          </div>

        )}

        {/* Loading */}

        {loading && (

          <div className="text-center py-5">

            <div
              className="spinner-border text-primary"
              role="status"
            >

              <span className="visually-hidden">
                Loading...
              </span>

            </div>

            <p className="text-secondary mt-3">
              Retrieving information...
            </p>

          </div>

        )}

        {/* Empty State */}

        {!loading && !error && results.length === 0 && (

          <div className="empty-state text-center p-5">

            <i className="bi bi-search display-5 text-secondary" />

            <h3 className="h6 mt-3">
              Nothing to display yet
            </h3>

            <p className="text-secondary mb-0">
              Submit a query to see your retrieved information here.
            </p>

          </div>

        )}

        {/* Search Results */}

        {!loading && results.map((item, index) => (

          <article
            className="result-card p-4 mb-3"
            key={item.id ?? item.url ?? index}
          >

            {/* Source and ID */}

            <div className="d-flex flex-wrap align-items-center gap-2 mb-2">

              <span className="badge text-bg-primary">
                {item.source ?? source}
              </span>

              {item.id != null && (

                <span className="text-secondary small">
                  ID: {item.id}
                </span>

              )}

            </div>

            {/* Title */}

            <h3 className="h5">
              {item.title ?? item.name ?? 'Untitled result'}
            </h3>

            {/* NLP Summary */}

            {item.summary && (

              <div className="summary-section mb-3">

                <strong>Summary</strong>

                <p className="result-text mb-0 mt-2">
                  {item.summary}
                </p>

              </div>

            )}

            {/* Article Preview */}

            {item.excerpt && (

              <div className="mb-3">

                <strong>Article Preview</strong>

                <p className="result-text mt-2 mb-0">
                  {item.excerpt}
                </p>

              </div>

            )}

            {/* Keywords */}

            {item.keywords?.length > 0 && (

              <div className="mb-3">

                <strong>Keywords</strong>

                <div className="mt-2">

                  {item.keywords.map((keyword) => (

                    <span
                      className="badge text-bg-secondary me-1 mb-1"
                      key={keyword}
                    >
                      {keyword}
                    </span>

                  ))}

                </div>

              </div>

            )}

            {/* Word Count */}

            {typeof item.word_count === 'number' && (

              <p className="text-secondary small mb-3">
                Word count: {item.word_count}
              </p>

            )}

            {/* Original Source */}

            {item.url && (

              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
              >
                View original source ↗
              </a>

            )}

          </article>

        ))}

      </section>

    </main>
  )
}

export default App
