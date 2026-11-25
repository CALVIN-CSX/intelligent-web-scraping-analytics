import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [query, setQuery] = useState('')
  const [source, setSource] = useState('web')
  const [limit, setLimit] = useState('20')

  const [results, setResults] = useState([])
  const [answer, setAnswer] = useState('')
  const [expandedQueries, setExpandedQueries] = useState([])
  const [parsedQuery, setParsedQuery] = useState(null)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const sourceNames = {
    web: 'Web',
    wikipedia: 'Wikipedia',
    pokemon: 'PokéAPI',
  }

  async function handleSearch(event) {
    event.preventDefault()

    if (!query.trim()) {
      setError('Please enter a search query.')
      return
    }

    setLoading(true)
    setError('')

    setResults([])
    setAnswer('')
    setExpandedQueries([])
    setParsedQuery(null)

    try {
      const response = await fetch(
        `${API_URL}/search?query=${encodeURIComponent(query)}&source=${encodeURIComponent(source)}&limit=${limit}`
      )

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(
          errorData.detail ?? `Request failed (${response.status})`
        )
      }

      const data = await response.json()

      setResults(data.results ?? [])
      setAnswer(data.answer ?? '')
      setExpandedQueries(data.expanded_queries ?? [])
      setParsedQuery(data.parsed_query ?? null)

    } catch (err) {
      setError(err.message || 'Could not retrieve results.')
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
          INTELLIGENT RESEARCH WORKSPACE
        </span>

        <h2 className="h4 mt-3 mb-2">
          What do you want to explore?
        </h2>

        <p className="text-secondary mb-4">
          Ask naturally. Discover relevant information through intelligent search.
        </p>

        <form onSubmit={handleSearch}>

          <div className="row g-2">

            {/* Search Input */}

            <div className="col-12 col-md">

              <input
                type="search"
                className="form-control form-control-lg"
                placeholder="Try important concepts in machine learning..."
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

                <option value="web">
                  Web Search
                </option>

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
              Relevant articles
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

            <div className="stat-value">
              {sourceNames[source] ?? source}
            </div>

          </div>

        </div>

      </section>

      {/* Error Message */}

      {error && (

        <div className="alert alert-danger" role="alert">
          {error}
        </div>

      )}

      {/* Loading */}

      {loading && (

        <div className="text-center py-5">

          <div className="spinner-border text-primary" role="status">

            <span className="visually-hidden">
              Loading...
            </span>

          </div>

          <p className="text-secondary mt-3">
            Understanding your query and retrieving relevant information...
          </p>

        </div>

      )}

      {/* Intelligent Search Information */}

      {!loading && parsedQuery && (

        <section className="result-card p-4 mb-4">

          <h2 className="h5 mb-3">
            <i className="bi bi-lightbulb me-2" />
            Query Understanding
          </h2>

          <div className="mb-3">

            <strong>Detected topic:</strong>

            <span className="ms-2">
              {parsedQuery.topic}
            </span>

          </div>

          <div className="mb-3">

            <strong>Detected intent:</strong>

            <span className="badge text-bg-primary ms-2">
              {parsedQuery.intent}
            </span>

          </div>

          {/* Expanded Queries */}

          {expandedQueries.length > 0 && (

            <div>

              <strong>Search variations:</strong>

              <div className="mt-2">

                {expandedQueries.map((item, index) => (

                  <span
                    className="badge text-bg-secondary me-2 mb-2"
                    key={index}
                  >
                    {item}
                  </span>

                ))}

              </div>

            </div>

          )}

        </section>

      )}

      {/* Consolidated Answer */}

      {!loading && answer && (

        <section className="result-card p-4 p-md-5 mb-4">

          <div className="d-flex align-items-center gap-2 mb-3">

            <i className="bi bi-stars fs-4" />

            <h2 className="h5 mb-0">
              Consolidated Answer
            </h2>

          </div>

          <div
            className="result-text"
            style={{ whiteSpace: 'pre-wrap' }}
          >
            {answer}
          </div>

          <p className="text-secondary small mt-3 mb-0">
            This answer is assembled from retrieved article content.
          </p>

        </section>

      )}

      {/* Search Results */}

      <section>

        <div className="d-flex align-items-center justify-content-between mb-3">

          <h2 className="h5 mb-0">
            Relevant Search Results
          </h2>

          <span className="text-secondary small">
            {results.length} items
          </span>

        </div>

        {/* Empty State */}

        {!loading && !error && results.length === 0 && !answer && (

          <div className="empty-state text-center p-5">

            <i className="bi bi-search display-5 text-secondary" />

            <h3 className="h6 mt-3">
              Nothing to display yet
            </h3>

            <p className="text-secondary mb-0">
              Submit a query to explore relevant information.
            </p>

          </div>

        )}

        {/* Ranked Results */}

        {!loading && results.map((item, index) => (

          <article
            className="result-card p-4 mb-3"
            key={item.id ?? item.url ?? index}
          >

            {/* Source and Rank */}

            <div className="d-flex flex-wrap align-items-center gap-2 mb-3">

              <span className="badge text-bg-primary">
                {item.source ?? sourceNames[source]}
              </span>

              <span className="badge text-bg-secondary">
                Rank #{index + 1}
              </span>

            </div>

            {/* Title */}

            <h3 className="h5">
              {item.title ?? item.name ?? 'Untitled result'}
            </h3>

            {/* Relevance Score */}

            {typeof item.relevance_score === 'number' && (

              <div className="mb-3">

                <div className="d-flex justify-content-between mb-1">

                  <strong>
                    Relevance
                  </strong>

                  <span>
                    {(item.relevance_score * 100).toFixed(1)}%
                  </span>

                </div>

                <div
                  className="progress"
                  role="progressbar"
                  aria-valuenow={item.relevance_score * 100}
                  aria-valuemin="0"
                  aria-valuemax="100"
                >

                  <div
                    className="progress-bar"
                    style={{
                      width: `${item.relevance_score * 100}%`
                    }}
                  />

                </div>

              </div>

            )}

            {/* Score Details */}

            {typeof item.semantic_score === 'number' && (

              <div className="d-flex flex-wrap gap-3 text-secondary small mb-3">

                <span>
                  Semantic score: {item.semantic_score.toFixed(4)}
                </span>

                {typeof item.normalized_keyword_score === 'number' && (

                  <span>
                    Keyword score: {item.normalized_keyword_score.toFixed(4)}
                  </span>

                )}

              </div>

            )}

            {/* Summary */}

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
                View original source &rarr;
              </a>

            )}

          </article>

        ))}

      </section>

    </main>
  )
}

export default App