import { useState } from 'react'
import { MapPin, Calendar, DollarSign, Plane, Building2, UtensilsCrossed, Mountain, PartyPopper, Loader2, Moon, Sun } from 'lucide-react'
import { useTheme } from './contexts/ThemeContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface Place {
  name: string
  description: string
  price: number
  category: string
}

interface ItineraryResponse {
  location: string
  days: number
  budget: number
  total_cost: number
  places: Record<string, Place[]>
}

interface TripRequest {
  location: string
  days: number
  budget: number
}

function App() {
  const { theme, toggleTheme } = useTheme()
  const [formData, setFormData] = useState<TripRequest>({
    location: '',
    days: 1,
    budget: 100
  })
  const [itinerary, setItinerary] = useState<ItineraryResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (field: keyof TripRequest, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/generate-itinerary`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate itinerary')
      }

      const data: ItineraryResponse = await response.json()
      setItinerary(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const getCategoryIcon = (categoryName: string) => {
    if (categoryName.includes('Historical')) return <Building2 className="h-5 w-5" />
    if (categoryName.includes('Food')) return <UtensilsCrossed className="h-5 w-5" />
    if (categoryName.includes('Scenic')) return <Mountain className="h-5 w-5" />
    if (categoryName.includes('Partying')) return <PartyPopper className="h-5 w-5" />
    return <MapPin className="h-5 w-5" />
  }

  const getCategoryColor = (categoryName: string) => {
    if (categoryName.includes('Historical')) return 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 border-blue-200 dark:border-blue-700'
    if (categoryName.includes('Food')) return 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 border-orange-200 dark:border-orange-700'
    if (categoryName.includes('Scenic')) return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border-green-200 dark:border-green-700'
    if (categoryName.includes('Partying')) return 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300 border-purple-200 dark:border-purple-700'
    return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-600'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8 relative">
          <button
            onClick={toggleTheme}
            className="absolute top-0 right-0 p-2 rounded-lg bg-white dark:bg-gray-800 shadow-md hover:shadow-lg transition-all duration-200 border border-gray-200 dark:border-gray-700"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? (
              <Moon className="h-5 w-5 text-gray-600 dark:text-gray-300" />
            ) : (
              <Sun className="h-5 w-5 text-yellow-500" />
            )}
          </button>
          <div className="flex items-center justify-center gap-2 mb-4">
            <Plane className="h-8 w-8 text-blue-600 dark:text-blue-400" />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white">Trippin</h1>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300">Plan your perfect trip with personalized itineraries</p>
        </div>

        <div className="max-w-2xl mx-auto mb-8">
          <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
                <MapPin className="h-5 w-5" />
                Plan Your Trip
              </CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-300">
                Enter your destination, trip duration, and budget to get a personalized itinerary
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="location" className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
                    <MapPin className="h-4 w-4" />
                    Destination
                  </Label>
                  <Input
                    id="location"
                    type="text"
                    placeholder="e.g., Paris, Tokyo, New York"
                    value={formData.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                    required
                    className="w-full bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="days" className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
                      <Calendar className="h-4 w-4" />
                      Number of Days
                    </Label>
                    <Input
                      id="days"
                      type="number"
                      min="1"
                      max="30"
                      value={formData.days}
                      onChange={(e) => handleInputChange('days', parseInt(e.target.value) || 1)}
                      required
                      className="w-full bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="budget" className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
                      <DollarSign className="h-4 w-4" />
                      Budget ($)
                    </Label>
                    <Input
                      id="budget"
                      type="number"
                      min="1"
                      step="0.01"
                      value={formData.budget}
                      onChange={(e) => handleInputChange('budget', parseFloat(e.target.value) || 100)}
                      required
                      className="w-full bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                    />
                  </div>
                </div>

                <Button 
                  type="submit" 
                  className="w-full bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white" 
                  disabled={loading || !formData.location.trim()}
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating Itinerary...
                    </>
                  ) : (
                    <>
                      <Plane className="mr-2 h-4 w-4" />
                      Generate Itinerary
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        {error && (
          <div className="max-w-2xl mx-auto mb-8">
            <Alert variant="destructive" className="bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
              <AlertDescription className="text-red-700 dark:text-red-400">{error}</AlertDescription>
            </Alert>
          </div>
        )}

        {itinerary && (
          <div className="max-w-6xl mx-auto">
            <div className="mb-6">
              <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between text-gray-900 dark:text-white">
                    <span>Your {itinerary.location} Itinerary</span>
                    <Badge variant="outline" className="text-lg px-3 py-1 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300">
                      {itinerary.days} {itinerary.days === 1 ? 'Day' : 'Days'}
                    </Badge>
                  </CardTitle>
                  <CardDescription className="flex items-center justify-between text-gray-600 dark:text-gray-300">
                    <span>Personalized recommendations for your trip</span>
                    <div className="text-right">
                      <div className="text-sm text-gray-600 dark:text-gray-400">Total Cost</div>
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                        ${itinerary.total_cost.toFixed(2)}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        Budget: ${itinerary.budget.toFixed(2)}
                      </div>
                    </div>
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {Object.entries(itinerary.places).map(([categoryName, places]) => (
                <Card key={categoryName} className="h-fit bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-gray-900 dark:text-white">
                      {getCategoryIcon(categoryName)}
                      {categoryName}
                    </CardTitle>
                    <CardDescription className="text-gray-600 dark:text-gray-300">
                      {places.length} {places.length === 1 ? 'recommendation' : 'recommendations'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {places.length > 0 ? (
                        places.map((place, index) => (
                          <div key={index} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4 hover:shadow-md transition-shadow bg-gray-50 dark:bg-gray-700">
                            <div className="flex items-start justify-between mb-2">
                              <h4 className="font-semibold text-gray-900 dark:text-white">{place.name}</h4>
                              <Badge className={getCategoryColor(categoryName)}>
                                ${place.price.toFixed(2)}
                              </Badge>
                            </div>
                            <p className="text-gray-600 dark:text-gray-300 text-sm">{place.description}</p>
                          </div>
                        ))
                      ) : (
                        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                          <p>No recommendations available for this category within your budget.</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
