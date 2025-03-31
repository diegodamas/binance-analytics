/*
* "e":"trade","E":1742925628705,"s":"BTCUSDT","t":4744236623,"p":"87890.27000000","q":"0.00007000","T":1742925628704,"m":false,"M":true
*/

package Dto;

import lombok.Data;

import java.sql.Timestamp;

@Data
public class Transaction {
    private String e; /*Event type*/
    private Timestamp E; /*Event time*/
    private String s; /*Symbol*/
    private Integer t; /*Trade ID*/
    private double p; /*Price*/
    private double q; /*Quantity*/
    private Timestamp T; /*Trade time*/
    private boolean m; /*Is the buyer the market maker?*/
    private boolean M; /*Ignore*/

}