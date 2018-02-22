#include <vector>
#include<math.h>
#include "genShadow.h"
#include "fitsio.h"
using namespace std;
#define NUMQUADRANT 1
#define COMP_COLS 270
#define PI 3.14159265
#define numElement 16
#define COLS 1950
#define ROWS 1950
#define TOTALROWS 8100
#define TOTALCOLS 8100
#define DET_NUMPIXELS 64
#define MASKFILENAME "/home/sysadm/czti/trunk/users/ajay/python_scripts/cross_correlation/compMask.fits"
void printerror( int status);
int checkbit(int *maskpattern,int i,int j);
void calculateTrans(float tx,float ty,float height,int *maskPattern,float * transValues);
void getMaskPattern(char*filename,int *buffer,int hduNo);
vector<double> getShadow (double tx,double ty,int quadid) {
  // compute average of each row..
  vector <double> averages; 

	int totalElements=TOTALROWS;
	int *maskElements=NULL,i=0,j=0,ii=0,jj=0,height=481,numelem=4096*NUMQUADRANT;	
	float *temp_exp;
	float pix_height,pix_width,ref_pix=2.46;
	maskElements=(int*)malloc(sizeof(int)*TOTALROWS*COMP_COLS);
	//shadow_pixels=(double*)malloc(sizeof(double)*DET_NUMPIXELS*DET_NUMPIXELS);
	temp_exp=(float*)malloc(sizeof(float)*DET_NUMPIXELS*DET_NUMPIXELS);
	 vector <double>shadow_pixels(numelem,0);
	if(maskElements==NULL||temp_exp==NULL)
	{
		printf("Error(%s:%d): Unable to allocate memory\n",__FILE__,__LINE__);
		exit(0);
	}
	for(i=0;i<NUMQUADRANT;i++)
	{
		getMaskPattern(MASKFILENAME,maskElements,quadid+2);
		calculateTrans(tx,ty,height,maskElements,temp_exp);
		for(ii=0;ii<DET_NUMPIXELS;ii++)
		{
			if(ii%16==0||(ii+1)%16==0)
			{
				pix_width=2.28;
			}
			else
			{
				pix_width=2.46;
			}
			pix_width/=ref_pix;
			for(jj=0;jj<DET_NUMPIXELS;jj++)
			{
				if(jj%16==0||(jj+1)%16==0)
				{
					pix_height=2.28;
				}
				else
				{
					pix_height=2.46;
				}	
				pix_height/=ref_pix;
				temp_exp[ii*DET_NUMPIXELS+jj]*=(pix_height*pix_width);
			}
		}
		for(j=0;j<DET_NUMPIXELS*DET_NUMPIXELS;j++)
		{
			shadow_pixels[(i*DET_NUMPIXELS*DET_NUMPIXELS)+j]=temp_exp[j];
			temp_exp[j-1]=0;
		}
		
	}

	free(maskElements);
	return shadow_pixels;

 //return averages;
}
void calculateTrans(float tx,float ty,float height,int *maskPattern,float * transValues)
{
	double xmin=0,ymin=0,x_open=0,y_open=0,totalOpen=0,trans=0,thetaX=0.0,thetaY=0.0,thickness=0.5;
	double mask_lower_left_x=0,mask_lower_left_y=0,x=0,y=0,x_mask=0,y_mask=0;;
	int i=0,j=0;
	char temp[100];
	thetaX=ty*(PI/180);
	thetaY=tx*(PI/180);
	int totalClose=0;
	int ii=0,jj=0;	
	long index=0;
	int yy=0,xx=0,yapitch=0,xpitch=0;
	int starty=0,startx=0,endy=0,endx=0;
	double lower_left_x=0,lower_left_y=0;
	int rowCounter=0,colCounter=0;	

	//All y's are X and all X's are y
	for(yy=0;yy<64;yy+=16,yapitch+=2)//this is for x
	{
	for(j=yy;j<(yy+16);j++)
	{
		
		starty=(COLS*(yy/16))+(yapitch/0.02);
		endy=(COLS*((yy/16)+1))+(yapitch/0.02);
		
		if(j==yy || j==yy+15)
		{
			rowCounter=114;
		}
		else
		{
			rowCounter=123;
		}
		lower_left_y=0;	
		
		for(xx=0,lower_left_y=0,xpitch=0;xx<64;xx+=16,xpitch+=2) //this is for y
		{
			for(i=xx;i<xx+16;i++)
			{
				
				startx=(COLS*(xx/16))+(xpitch/0.02);
				endx=(COLS*((xx/16)+1))+(xpitch/0.02);
				
				if(i==xx || i==xx+15)
				{
					colCounter=114;
				}
				else
				{
					colCounter=123;
				}

				x=lower_left_y;
				y=lower_left_x;
				//printf("X=%f\tY=%f\n",x,y);
				x_mask=x+(height*(tan(thetaX)));
				y_mask=y+(height*(tan(thetaY)));
				x_mask/=0.02;
				y_mask/=0.02;	
				totalOpen=0;
				
				for(jj=(int)y_mask;jj<(int)y_mask+rowCounter;jj++,index++)//this is for x
				{
				for(ii=(int)x_mask;ii<(int)x_mask+colCounter;ii++)// this is for y
				{
						if(jj>=starty && jj<endy && ii>=startx && ii<endx)
						{
							if(checkbit(maskPattern,ii,jj))
							{
								totalOpen++;
							}
							else
							{
								totalClose++;
							}
						}
				}
				}	
				transValues[i*DET_NUMPIXELS+j]=totalOpen/(colCounter*rowCounter);
				float thickBlockage=(thickness*tan(thetaY));//(thickness*tan(thetaY)));
				
				if(thickBlockage<0)
				{
					thickBlockage*=-1;	
				}	
				if(transValues[i*DET_NUMPIXELS+j]-thickBlockage<=0)
				{
					transValues[i*DET_NUMPIXELS+j]=0;
				}				
				else
				{
					transValues[i*DET_NUMPIXELS+j]-=thickBlockage;
				}
				thickBlockage=(thickness*tan(thetaX));
				if(thickBlockage<0)
				{
					thickBlockage*=-1;	
				}	
				if(transValues[i*DET_NUMPIXELS+j]-thickBlockage<=0)
				{
					transValues[i*DET_NUMPIXELS+j]=0;
				}				
				else
				{
					transValues[i*DET_NUMPIXELS+j]-=thickBlockage;
				}

				if(transValues[i*DET_NUMPIXELS+j]>1 || transValues[i*DET_NUMPIXELS+j]<0)
				{
					printf("Error:(%s:%d):Abnormal Trans value=%f\n",__FILE__,__LINE__,transValues[i*DET_NUMPIXELS+j]);
					exit(0);
				}
				if(i==xx || i==xx+15)
				{
					lower_left_y+=2.28;
				}
				else
				{
					lower_left_y+=2.46;
				}
			}
			lower_left_y+=2;
		}//end loop for y
		if(j==yy || j==yy+15)
		{
			lower_left_x+=2.28;
		}
		else
		{
			lower_left_x+=2.46;
		}
	}
		lower_left_x+=2;
	}//end loop for x
}
int checkbit(int *maskpattern,int i,int j)
{
	
	int temp_val=0,jj=0,bit_no=0;
	jj=j/30;
	bit_no=j%30;
	temp_val=maskpattern[i*COMP_COLS+jj];	
	if(temp_val&=(1<<bit_no))
	{
		return 1;
	}
	else
	{
		return 0;
	}	
}
void getMaskPattern(char*filename,int *buffer,int hduNo)
{
	fitsfile *fptr;       /* pointer to the FITS file, defined in fitsio.h */
    	int status,  nfound, anynull,hdutype,i,j;
    	long naxes[2], fpixel, nbuffer, npixels, ii;
    	float datamin, datamax, nullval;
    	status = 0;

    	if ( fits_open_file(&fptr, filename, READONLY, &status) )
    		printerror( status );

   	if ( fits_movabs_hdu(fptr, hduNo, &hdutype, &status) ) 
   		printerror( status );
	
    	if ( fits_read_keys_lng(fptr, "NAXIS", 1, 2, naxes, &nfound, &status) )
        	printerror( status );
	 
    	npixels  = naxes[0] * naxes[1];         /* number of pixels in the image */
    	fpixel   = 1;
    	nullval  = 0;                /* don't check for null values in the image */
	while (npixels > 0)
    	{
      		nbuffer = npixels;
      		if ( fits_read_img(fptr, TINT, fpixel, nbuffer, &nullval,buffer, &anynull, &status) )
           		printerror( status ); 
      		npixels -= nbuffer;    
      		fpixel  += nbuffer;    
    	}
    	if ( fits_close_file(fptr, &status) )
        	printerror( status );
    	return;
}
void printerror( int status)
{
    if (status)
    {
       fits_report_error(stderr, status); /* print error report */
       exit( status );    /* terminate the program, returning error status */
    }
    return;
}

