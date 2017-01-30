using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace BlockFortressMapEditor.LevelModel
{
    /// <summary>
    /// Container class for level data
    /// </summary>
    class LevelData
    {
        /// <summary>
        /// Gets the name
        /// </summary>
        public string Name { get; private set; }
        
        /// <summary>
        /// Gets the visibility
        /// </summary>
        public bool Visible { get; private set; }
        
        /// <summary>
        /// Returns a new instance
        /// </summary>
        /// <param name="name">Name of data</param>
        /// <param name="visible">Visibility of data</param>
        public LevelData(string name, bool visible)
        {
            Name = name;
            Visible = visible;
        }
    }
}
