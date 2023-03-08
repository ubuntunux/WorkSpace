//	
//	============================================================
//	Name:		Jiggle Bone v.1.0
//	Author: 	Michael Cook (Fishypants)
//	Date:		9-25-2011
//	License:	Free to use. Any credit would be nice :)
//	
//	To Use:
//	Drag this script onto a bone. (ideally bones at the end)
//	Set the boneAxis to be the front facing axis of the bone.
//	Done! Now you have bones with jiggle dynamics.
//	
//	============================================================


// Modified by SangWon Lee, 2015-03-27
// Why? -- 8ds Max bone axis friendly

using UnityEngine;
using System.Collections;

public class JiggleBoneMax: MonoBehaviour {
	public bool debugMode = true;
	
	// Target and dynamic positions
	//Vector3 targetPos = new Vector3();
	Vector3 dynamicPos = new Vector3();
	
	// Bone settings
	[HideInInspector]		// My code
	public Vector3 boneAxis = new Vector3(1,0,0);		// My code, Original was new Vector3(0,0,1)
	public float targetDistance = 2.0f;
	
	// Dynamics settings
	public float bStiffness = 0.1f;
	public float bMass = 0.9f;
	public float bDamping = 0.75f;
	public float bGravity = 0.0f;
	
	// Dynamics variables
	Vector3 force = new Vector3();
	Vector3 acc = new Vector3();
	Vector3 vel = new Vector3();
	
	// Squash and stretch variables
	public bool SquashAndStretch = false;
	public float sideStretch = 0.15f;
	public float frontStretch = 0.2f;

    private Transform _trans;		// My code, 'transform' to '_trans' replace
	
	void Awake(){

        _trans = transform;        

		// Set targetPos and dynamicPos at startup
		boneAxis.x = boneAxis.x * -1;		// My code
		Vector3 targetPos = _trans.position + _trans.TransformDirection(new Vector3((boneAxis.x * targetDistance),(boneAxis.y * targetDistance),(boneAxis.z * targetDistance)));
		dynamicPos = targetPos;
	}
	
	void LateUpdate(){
		// Reset the bone rotation so we can recalculate the upVector and forwardVector
		_trans.rotation = new Quaternion();

		// Update forwardVector and upVector
		Vector3 forwardVector = _trans.TransformDirection(new Vector3((boneAxis.x * targetDistance),(boneAxis.y * targetDistance),(boneAxis.z * targetDistance)));
		Vector3 upVector = _trans.TransformDirection(new Vector3(0,1,0));

		// Calculate target position
		Vector3 targetPos = _trans.position + _trans.TransformDirection(new Vector3((boneAxis.x * targetDistance),(boneAxis.y * targetDistance),(boneAxis.z * targetDistance)));
		
		// Calculate force, acceleration, and velocity per X, Y and Z
		force.x = (targetPos.x - dynamicPos.x) * bStiffness;
		acc.x = force.x / bMass;
		vel.x += acc.x * (1 - bDamping);
		
		force.y = (targetPos.y - dynamicPos.y) * bStiffness;
		force.y -= bGravity / 10; // Add some gravity
		acc.y = force.y / bMass;
		vel.y += acc.y * (1 - bDamping);
		
		force.z = (targetPos.z - dynamicPos.z) * bStiffness;
		acc.z = force.z / bMass;
		vel.z += acc.z * (1 - bDamping);
		
		// Update dynamic postion
		dynamicPos += vel + force;
		
		// Set bone rotation to look at dynamicPos
		_trans.LookAt(dynamicPos, upVector);
		_trans.Rotate(0, 90, 0);		// My code

		//My debugcode 
		//transform.LookAt(GameObject.Find ( "dPos" ).transform.position, GameObject.Find ( "up" ).transform.position);
		//GameObject.Find ( "dPos" ).transform.position = dynamicPos;
		//GameObject.Find ( "up" ).transform.position = upVector * 5;
				
		// ==================================================
		// Squash and Stretch section
		// ==================================================
		if(SquashAndStretch){
			// Create a vector from target position to dynamic position
			// We will measure the magnitude of the vector to determine
			// how much squash and stretch we will apply
			Vector3 dynamicVec = dynamicPos - targetPos;
			
			// Get the magnitude of the vector
			float stretchMag = dynamicVec.magnitude;
			
			// Here we determine the amount of squash and stretch based on stretchMag
			// and the direction the Bone Axis is pointed in. Ideally there should be
			// a vector with two values at 0 and one at 1. Like Vector3(0,0,1)
			// for the 0 values, we assume those are the sides, and 1 is the direction
			// the bone is facing
			float xStretch;
			if(boneAxis.x == 0) xStretch = 1 + (-stretchMag * sideStretch);
			else xStretch = 1 + (stretchMag * frontStretch);
			
			float yStretch;
			if(boneAxis.y == 0) yStretch = 1 + (-stretchMag * sideStretch);
			else yStretch = 1 + (stretchMag * frontStretch);
			
			float zStretch;
			if(boneAxis.z == 0) zStretch = 1 + (-stretchMag * sideStretch);
			else zStretch = 1 + (stretchMag * frontStretch);
			
			// Set the bone scale
			_trans.localScale = new Vector3(xStretch, yStretch, zStretch);

		}
		
		// ==================================================
		// DEBUG VISUALIZATION
		// ==================================================
		// Green line is the bone's local up vector
		// Blue line is the bone's local foward vector
		// Yellow line is the target postion
		// Red line is the dynamic postion
		if(debugMode){
			Debug.DrawRay(transform.position, forwardVector, Color.blue);
			Debug.DrawRay(transform.position, upVector, Color.green);
			Debug.DrawRay(targetPos, Vector3.up * 0.2f, Color.yellow);
			Debug.DrawRay(dynamicPos, Vector3.up * 0.2f, Color.red);
		}
		// ==================================================
	}
}