using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace BlockFortressMapEditor.LevelModel
{
    /// <summary>
    /// Represents a game level
    /// </summary>
    class Level
    {
        private const LevelData defaultValue = null;

        /// <summary>
        /// Gets the current level width
        /// </summary>
        public int Width { get; private set; }
        
        /// <summary>
        /// Gets the current level height
        /// </summary>
        public int Height { get; private set; }

        private LevelData[,] levelArray;

        /// <summary>
        /// Creates an instance of Level with the specified dimensions, with all data set to the default value
        /// </summary>
        /// <param name="width">Width of level</param>
        /// <param name="height">Height of level</param>
        public Level(int width, int height)
        {
            Width = width;
            Height = height;
            levelArray = new LevelData[width, height];
            Reset();
        }

        /// <summary>
        /// Resets the level to original values
        /// </summary>
        public void Reset()
        {
            for (int i = 0; i < Width; i++)
            {
                for (int j = 0; j < Height; j++)
                {
                    levelArray[i, j] = defaultValue;
                }
            }
        }

        /// <summary>
        /// Returns the data of the level at the given coordinate
        /// </summary>
        /// <param name="posX">X coordinate</param>
        /// <param name="posY">Y coordinate</param>
        /// <returns>Level data for the provided coordinate</returns>
        public LevelData GetData(int posX, int posY)
        {
            if (CoordinateValid(posX, posY))
            {
                return levelArray[posX, posY];
            }
            else
            {
                throw new ArgumentException("Coordinate must be within level size!");
            }
        }

        /// <summary>
        /// Sets the level data at a given coordinate
        /// </summary>
        /// <param name="posX">X coordinate</param>
        /// <param name="posY">Y coordinate</param>
        /// <param name="data">The data to set</param>
        public void SetData(int posX, int posY, LevelData data)
        {
            if (CoordinateValid(posX, posY))
            {
                levelArray[posX, posY] = data;
            }
            else
            {
                throw new ArgumentException("Coordinate must be within level size!");
            }
        }

        private bool CoordinateValid(int posX, int posY)
        {
            return posX >= 0 && posX < Width
                && posY >= 0 && posY < Height;
        }
    }
}
