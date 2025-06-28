import React, { useState, useEffect } from 'react';
import Grid from '../components/Grid';

interface Activity {
  id: number;
  name: string;
  color: string;
  icon: string;
}

const Dashboard: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [activities, setActivities] = useState<Activity[]>([
    { id: 1, name: 'Exercise', color: '#3B82F6', icon: '💪' },
    { id: 2, name: 'Read', color: '#10B981', icon: '📚' },
    { id: 3, name: 'Meditate', color: '#8B5CF6', icon: '🧘' },
    { id: 4, name: 'Work', color: '#F59E0B', icon: '💼' },
    { id: 5, name: 'Social', color: '#EF4444', icon: '👥' },
  ]);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [loggedActivities, setLoggedActivities] = useState<Record<string, number>>({});
  const [gridSize, setGridSize] = useState(16);

  const handleCellClick = (position: number) => {
    if (selectedActivity) {
      setLoggedActivities(prev => ({
        ...prev,
        [position.toString()]: selectedActivity.id
      }));
      setSelectedActivity(null);
    }
  };

  const handleActivitySelect = (activity: Activity) => {
    setSelectedActivity(activity);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Daily Habit Grid
        </h1>
        <p className="text-gray-600">
          Click on an activity below, then tap a grid cell to log it
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Activity Selector */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              Activities
            </h2>
            <div className="space-y-3">
              {activities.map((activity) => (
                <button
                  key={activity.id}
                  onClick={() => handleActivitySelect(activity)}
                  className={`
                    w-full p-3 rounded-lg border-2 transition-all duration-200
                    flex items-center space-x-3 text-left
                    ${selectedActivity?.id === activity.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }
                  `}
                >
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm"
                    style={{ backgroundColor: activity.color }}
                  >
                    {activity.icon}
                  </div>
                  <span className="font-medium text-gray-800">
                    {activity.name}
                  </span>
                </button>
              ))}
            </div>

            {/* Grid Size Selector */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                Grid Size
              </h3>
              <div className="space-y-2">
                {[
                  { size: 16, label: '4×4 Grid' },
                  { size: 36, label: '6×6 Grid' },
                  { size: 64, label: '8×8 Grid' },
                ].map((option) => (
                  <button
                    key={option.size}
                    onClick={() => setGridSize(option.size)}
                    className={`
                      w-full p-2 rounded text-left transition-colors
                      ${gridSize === option.size
                        ? 'bg-blue-100 text-blue-700'
                        : 'hover:bg-gray-100'
                      }
                    `}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Grid Display */}
        <div className="lg:col-span-2">
          <Grid
            date={selectedDate}
            gridSize={gridSize}
            activities={activities}
            loggedActivities={loggedActivities}
            onCellClick={handleCellClick}
            selectedActivity={selectedActivity}
          />
        </div>
      </div>

      {/* Instructions */}
      <div className="mt-8 bg-blue-50 rounded-lg p-4">
        <h3 className="font-semibold text-blue-800 mb-2">How to use:</h3>
        <ol className="text-blue-700 text-sm space-y-1">
          <li>1. Select an activity from the left panel</li>
          <li>2. Click on any empty grid cell to log that activity</li>
          <li>3. Watch your daily pattern emerge as you fill the grid</li>
          <li>4. Each colored square represents a completed activity</li>
        </ol>
      </div>
    </div>
  );
};

export default Dashboard; 