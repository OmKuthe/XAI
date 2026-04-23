// components/Header.jsx - Alternative with different colored badges
const Header = () => {
    return (
      <header className="bg-gradient-to-r from-blue-700 to-purple-700 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6 max-w-7xl">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="text-4xl">🎯</div>
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-white">XAI Event Recommender</h1>
                <p className="text-blue-100 text-sm">Explainable AI for Personalized Event Discovery</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm">
              {/* Different colors for each badge */}
              <span className="px-3 py-1 bg-blue-500 rounded-full text-white">
                🤖 AI-Powered
              </span>
              <span className="px-3 py-1 bg-purple-500 rounded-full text-white">
                📊 XAI Enabled
              </span>
              <span className="px-3 py-1 bg-green-500 rounded-full text-white">
                🎓 Final Year Project
              </span>
            </div>
          </div>
        </div>
      </header>
    );
  };
  
  export default Header;