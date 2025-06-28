import React, { useState } from 'react';

interface Activity {
  id: number;
  name: string;
  color: string;
  icon: string;
}

interface GridProps {
  date: string;
  gridSize: number;
  activities: Activity[];
  loggedActivities: Record<string, number>;
  onCellClick: (position: number) => void;
  selectedActivity?: Activity | null;
}

const Grid: React.FC<GridProps> = ({
  date,
  gridSize,
  activities,
  loggedActivities,
  onCellClick,
  selectedActivity
}) => {
  const [hoveredCell, setHoveredCell] = useState<number | null>(null);
  
  // Calculate grid dimensions
  const getGridDimensions = (size: number) => {
    switch (size) {
      case 16: return { rows: 4, cols: 4 };
      case 36: return { rows: 6, cols: 6 };
      case 64: return { rows: 8, cols: 8 };
      default: return { rows: 4, cols: 4 };
    }
  };
  
  const { rows, cols } = getGridDimensions(gridSize);
  
  const getActivityAtPosition = (position: number): Activity | null => {
    const activityId = loggedActivities[position.toString()];
    if (activityId) {
      return activities.find(activity => activity.id === activityId) || null;
    }
    return null;
  };
  
  const renderCell = (position: number) => {
    const activity = getActivityAtPosition(position);
    const isHovered = hoveredCell === position;
    const isSelected = selectedActivity && !activity;
    
    return (
      <div
        key={position}
        className={`
          grid-cell w-12 h-12 rounded-lg border-2 cursor-pointer
          flex items-center justify-center text-white font-bold text-sm
          transition-all duration-200 ease-in-out
          ${activity 
            ? 'border-transparent shadow-md' 
            : 'border-gray-300 bg-gray-100 hover:bg-gray-200'
          }
          ${isHovered ? 'scale-110 z-10' : ''}
          ${isSelected ? 'border-blue-500 bg-blue-100' : ''}
        `}
        style={{
          backgroundColor: activity ? activity.color : undefined,
          transform: isHovered ? 'scale(1.1)' : 'scale(1)',
        }}
        onClick={() => onCellClick(position)}
        onMouseEnter={() => setHoveredCell(position)}
        onMouseLeave={() => setHoveredCell(null)}
        title={activity ? activity.name : 'Click to log activity'}
      >
        {activity ? activity.icon : ''}
      </div>
    );
  };
  
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-gray-800">
          {new Date(date).toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          })}
        </h2>
        <p className="text-gray-600 text-sm">
          Grid: {rows}×{cols} ({gridSize} cells)
        </p>
      </div>
      
      <div 
        className="grid gap-2 mx-auto"
        style={{
          gridTemplateColumns: `repeat(${cols}, 1fr)`,
          maxWidth: `${cols * 60 + (cols - 1) * 8}px`
        }}
      >
        {Array.from({ length: gridSize }, (_, index) => renderCell(index))}
      </div>
      
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-600">
          Completion: {Object.keys(loggedActivities).length}/{gridSize} (
          {Math.round((Object.keys(loggedActivities).length / gridSize) * 100)}%)
        </p>
      </div>
    </div>
  );
};

export default Grid; 